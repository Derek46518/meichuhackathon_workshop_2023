from . import bp
from flask import Response
from common import logging
from flask import request
from ..metricss import custom_metrics


_logger = logging.getLogger("config")

# 底下先宣告在哪個路徑 並且宣告為post method
@bp.route('/upload', methods=['POST'])
def upload_image():
    # TODO
    if 'images' in request.files:
        image = request.files['images']
    _logger.info(image.filename)

    image.save('./aaa.jpg')
    if 'aaa' in image.filename:
        custom_metrics.abnormal_counter.inc()
        return Response("e",404)
    return Response("AAVBB", 200)
