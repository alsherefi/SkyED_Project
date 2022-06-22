from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import get_template
from PIL import Image, ImageDraw
import base64
import qrcode
import qrcode.image.svg
from io import BytesIO

def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None

def generate_qrcode_for_pdf(qrurl, img_size):
	qrcode_box_size = img_size // 37
	qrcode_img = qrcode.make(qrurl, box_size=qrcode_box_size)
	canvas = Image.new('RGB', (img_size, img_size), 'white')
	draw = ImageDraw.Draw(canvas)
	canvas.paste(qrcode_img)
	buffer = BytesIO()
	canvas.save(buffer, 'PNG')
	return base64.b64encode(buffer.getvalue()).decode('utf8')

def generate_qrcode(qrurl):

	factory = qrcode.image.svg.SvgImage
	img = qrcode.make(qrurl, image_factory=factory, box_size=10)
	stream = BytesIO()
	img.save(stream)
	return stream.getvalue().decode()


	
