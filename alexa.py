# -*- coding: utf-8 -*-

import logging
import ask_sdk_core.utils as ask_utils
import json
import requests
from funcion import scrapper
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


CONVERTIR = {'director':'Dirección', 'guionistas':'Guionistas', 'elenco':'Elenco', 'nota': 'puntuación'}

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speak_output = "Buenos días, ¿qué información quiere de qué película?"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class ObtenerDatoPeliculaIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return handler_input.request_envelope.request.intent.name == "ObtenerDatoPeliculaIntent"

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        dato = slots["Dato"].value
        pelicula = slots["Pelicula"].value
        # Llamar al scraper
        data = scrapper(pelicula)
        
        # Arreglamos llamadas
        if dato in CONVERTIR.keys():
            dato = CONVERTIR[dato]
            
        # Capturamos error
        if dato not in data.keys():
            salida = f'No se encuentra {dato}' + str(data)
        # Construir la respuesta
        elif dato in ['número de votos', 'director']:
            speech_text = f"El {dato} de {pelicula} es {data[dato]}"
        else:
            speech_text = f"La {dato} de {pelicula} es {data[dato]}"
        
        return handler_input.response_builder.speak(salida).response

class ObtenerSinopsisIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return handler_input.request_envelope.request.intent.name == "ObtenerSinopsisIntent"

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        pelicula = slots["Pelicula"].value
        
        # Llamar al scraper
        data = scrapper(pelicula)
        
        # Construir la respuesta
        speech_text = f"La sinopsis de {pelicula} es {data['sinopsis']}"
        
        return handler_input.response_builder.speak(speech_text).response

class ObtenerVotosIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return handler_input.request_envelope.request.intent.name == "ObtenerVotosIntent"

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        pelicula = slots["Pelicula"].value
        
        # Llamar al scraper
        data = scrapper(pelicula)
        
        # Construir la respuesta
        speech_text = f"{pelicula} tiene {data['número de votos']} votos"
        
        return handler_input.response_builder.speak(speech_text).response

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = "You can say hello to me! How can I help?"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        speak_output = "Goodbye!"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"
        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # Any cleanup logic goes here.
        return handler_input.response_builder.response

class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request handler chain below.
    """
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors.
    If you receive an error stating the request handler chain is not found,
    you have not implemented a handler for the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        logger.error(exception, exc_info=True)
        speak_output = 'Ha habido un error'
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

sb = SkillBuilder() 

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(ObtenerDatoPeliculaIntentHandler())
sb.add_request_handler(ObtenerSinopsisIntentHandler())
sb.add_request_handler(ObtenerVotosIntentHandler())
sb.add_request_handler(IntentReflectorHandler())  # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()