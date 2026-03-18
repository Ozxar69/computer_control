import logging

from fastapi import APIRouter

from keyboard.keyboard import play_pause

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/play-pause")
def keyboard_play_pause():
    play_pause()
    logger.info("Play/Pause triggered")
    return {"success": True}
