import logging
from typing import Dict, List, Union

from flask import request, Blueprint, Response, render_template, abort

from config import Setting
from line.game_flex import (
    scoreboard_contents,
    match_contents,
)
from line.standing_flex import (
    standing_content,
)

settings = Setting()
logger = logging.getLogger(__name__)

liff_blueprint = Blueprint('liff', __name__, )


@liff_blueprint.route("/liff/share", methods=['GET'])
def liff_page():
    if request.args.get("liff.state"):
        return Response(render_template('liff_redirect.html', liff_id=settings.LIFF_SHARE_ID))

    abort(404)


@liff_blueprint.route("/liff/share/<string:action>", methods=['GET'])
def liff_share_standing(action):

    # TODO: add me flex for default
    alt = "分享CPBL戰績排行"
    contents = standing_content(footer=False)
    flex = flex_json(alt, contents)

    if action == "standing":
        alt = "分享CPBL戰績排行"
        contents = standing_content(footer=False)
        flex = flex_json(alt, contents)

    elif action == "match":
        alt = "分享CPBL今日賽事"
        contents = match_contents(footer=False)
        flex = flex_json(alt, contents)

    elif action == "score":
        alt = "分享CPBL即時比數"
        contents = scoreboard_contents(footer=False)
        flex = flex_json(alt, contents)

    return Response(render_template('share_message.html', flex=flex, liff_id=settings.LIFF_SHARE_ID))


def flex_json(alt: str, content: Union[Dict, List[Dict]]):
    if isinstance(content, dict):
        content = [content]
    return {
        "type": "flex",
        "altText": alt,
        "contents": {
            **{
                "type": "carousel",
                "contents": content
            }
        }
    }
