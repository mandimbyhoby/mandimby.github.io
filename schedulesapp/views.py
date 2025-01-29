from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Schedule, ClientRegistration
import logging
import stripe
from django.conf import settings
from django.http import JsonResponse


def schedule_view(request):
    if request.method == 'POST':
        # Récupérer les données du formulaire
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        program_id = request.POST.get('program_id')

        # Récupérer l'horaire en utilisant program_id
        schedule = get_object_or_404(Schedule, id=program_id)

        # Gérer la case à cocher pour le paiement
        payment_on_day = request.POST.get('payment_day') == 'on'

        # Vérifier si le programme est complet
        current_participants = ClientRegistration.objects.filter(schedule=schedule).count()
        if current_participants >= schedule.max_participants:
            messages.error(request, 'Ce cours est complet. Veuillez choisir un autre.')
            return render(request, 'schedules.html', {'schedules': Schedule.objects.all()})

        # Inscrire l'utilisateur au cours
        ClientRegistration.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            contact=contact,
            schedule=schedule,
            payment_on_day=payment_on_day
        )

        # Afficher un message de succès
        messages.success(request, 'Vous vous êtes inscrit avec succès au cours !')
        return redirect('/schedules/#alertSection')

    # Si la méthode de requête n'est pas POST, charger toutes les classes
    schedules = Schedule.objects.all()
    return render(request, 'schedules.html', {'schedules': schedules})


logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

def register_user(request):
    if request.method == 'POST':
        logger.info(f"Form data: {request.POST}")

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        program_id = request.POST.get('program_id')
        payment_on_day = request.POST.get('payment_day', False)

        # Validate required fields
        if not all([first_name, last_name, email, contact, program_id]):
            messages.error(request, 'Veuillez remplir tous les champs.')
            return redirect('/schedules/#alertSection')

        # Retrieve the selected schedule
        schedule = get_object_or_404(Schedule, id=program_id)

        # Check if the program is full
        current_participants = ClientRegistration.objects.filter(schedule=schedule).count()
        logger.info(f"Current participants for {schedule.name}: {current_participants}")

        if current_participants >= schedule.max_participants:
            messages.error(request, 'Ce cours est complet. Veuillez choisir un autre.')
            return redirect('/schedules/#alertSection')

        # If the user has chosen to pay on the day, register without Stripe payment
        if payment_on_day:
            registration = ClientRegistration.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                contact=contact,
                schedule=schedule,
                payment_on_day=True  # Payment will be made on the day of the session
            )
            logger.info(f"Registration created: {registration.id}")
            messages.success(request, 'Vous vous êtes inscrit avec succès au cours !')
            return redirect('/schedules/#alertSection')

        # Otherwise, proceed with Stripe payment
        try:
            payment_method_id = request.POST.get('payment_method_id')

            if not payment_method_id:
                messages.error(request, 'Aucune méthode de paiement n\'a été fournie.')
                return redirect('/schedules/#alertSection')

            # Create a PaymentIntent with Stripe
            payment_intent = stripe.PaymentIntent.create(
                amount=1000,  # Amount in cents, adjust based on your pricing (e.g., 1000 = 10 EUR)
                currency='eur',
                payment_method=payment_method_id,  # ID of the payment method from the frontend
                confirmation_method='manual',
                confirm=True,  # Immediately confirm the PaymentIntent
            )

            # If payment is successful, register the user
            if payment_intent['status'] == 'succeeded':
                registration = ClientRegistration.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    contact=contact,
                    schedule=schedule,
                    payment_on_day=False,  # Payment made online
                    stripe_payment_id=payment_intent['id']
                )
                logger.info(f"Registration created: {registration.id}")
                messages.success(request, 'Vous vous êtes inscrit avec succès au cours !')
                return redirect('/schedules/#alertSection')
            else:
                # If payment is not completed, return an error
                messages.error(request, 'Le paiement a échoué. Veuillez réessayer.')
                return redirect('/schedules/#alertSection')

        except stripe.error.CardError as e:
            messages.error(request, 'Erreur de paiement Stripe : {}'.format(e.error.message))
            logger.error(f"Stripe card error: {str(e)}")
            return redirect('/schedules/#alertSection')

        except stripe.error.StripeError as e:
            messages.error(request, 'Une erreur est survenue lors du traitement du paiement. Veuillez réessayer.')
            logger.error(f"Stripe error: {str(e)}")
            return redirect('/schedules/#alertSection')

    # If the request is not POST, render the form
    schedules = Schedule.objects.all()
    return render(request, 'schedules.html', {'schedules': schedules})