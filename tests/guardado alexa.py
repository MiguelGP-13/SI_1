
class ObtenerDatoPeliculaIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return handler_input.request_envelope.request.intent.name == "ObtenerDatoPeliculaIntent"

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        dato = slots["Dato"].value
        pelicula = slots["Pelicula"].value
        
        # Llamar al scraper
        data = scrapper(pelicula)
        
        # Construir la respuesta
        if dato in ['número de votos', 'director']:
            speech_text = f"El {dato} de {pelicula} es {data[dato]}"
        else:
            speech_text = f"La {dato} de {pelicula} es {data[dato]}"
        
        return handler_input.response_builder.speak(speech_text).response

class SinopsisIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return handler_input.request_envelope.request.intent.name == "SinopsisIntent"

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        pelicula = slots["Pelicula"].value
        
        # Llamar al scraper
        data = scrapper(pelicula)
        
        # Construir la respuesta
        speech_text = f"La sinopsis de {pelicula} es {data['sinopsis']}"
        
        return handler_input.response_builder.speak(speech_text).response


