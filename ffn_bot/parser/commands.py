import logging
from .parser import parser, RequestParser
from ffn_bot.state import Application


@RequestParser.register(50)
@parser(lambda request: 'delete' in request.markers)
def delete_command(request):
    Application().comments.add(str(request.identifier))
    logging.info("Delete requested by " + request.identifier)
    if request.parent is None:
        logging.error("Delete requested by invalid comment!")
        return

    parent_comment = request.parent
    if parent_comment.request.author is None:
        logging.error("Delete requested on null comment.")
        return
    if parent_comment.request.author.name != Application().bot_parameters['user']:
        logging.error("Delete requested on non-bot comment!")
        return

    logging.info("Deleting comment " + parent_comment.id)
    parent_comment.request.delete()

    return False
