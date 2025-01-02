from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import qrcode
from io import BytesIO

from shortener.models import URL


def generate_qr(request, short_url):
    """
    Generate a QR code for the provided short URL.

    This view retrieves the original URL associated with the provided short URL
    from the database and generates a QR code for it. The QR code image is
    returned as a PNG response.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :param short_url: The short URL string to resolve to the original URL.
    :type short_url: str
    :return: An HTTP response containing the QR code image as a PNG.
    :rtype: HttpResponse
    """
    # Retrieve the URL object from the database
    url_obj = get_object_or_404(URL, short_url=short_url)

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url_obj.original_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Save QR code image to buffer
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # Return the QR code image as an HTTP response
    return HttpResponse(buffer.getvalue(), content_type="image/png")
