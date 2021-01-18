import os
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa

from .models import CompraEnc, CompraDet
from django.utils import timezone

def link_callback(uri, rel):
	"""
		Convert URL to absolute system paths os xhtml2pdf can access those resources
	"""
	# use short variable names
	sUrl = settings.STATIC_URL 		# Typically /static/
	sRoot = settings.STATIC_ROOT 	# Typically /home/userX/project_static/
	mUrl = settings.MEDIA_URL 		# Ttpically /home/userX/project_static/
	mRoot = settings.MEDIA_ROOT 	# Ttpically /home/userX/project_static/media/

	# convert URIs to absolute system paths
	if uri.startwith(mUrl):
		path = os.path.join(mRoot, uri.replace(mUrl, ""))
	elif uri.startwith(sUrl):
		path = os.path.join(sRoot, uri.replace(sUrl, ""))
	else:
		return uri # handle absolute url (ie: http:://some.tld/foo.png)


	# make sure that file exists
	if not os.path.isfile(path):
		raise Exception(
			'media URI must start with %s or %s' % (sUrl, mUrl)
		)
	return path

def reporte_compras(request):
	template_path = "cmp/compras_print_all.html"
	today = timezone.now()

	compras = CompraEnc.objects.all()

	context = {
		"obj": compras,
		"today": today,
		"request": request
	}

	# Create a Django response object, and specify content_type as pdf
	response = HttpResponse(content_type = "application/pdf")
	response["Content-Disposition"] = "inline; filename='todas_compras.pdf'"
	template = get_template(template_path)
	html = template.render(context)

	# create a pdf
	pisaStatus = pisa.CreatePDF(
		html, dest = response, link_callback = link_callback
	)
	# if error then show some funy view
	if pisaStatus.err:
		return HttpResponse("We had some errors <pre>"+ html +"</pre>")
	return response


def imprimir_compra(request, compra_id):
	template_path = "cmp/compras_print_one.html"
	today = timezone.now()

	enc = CompraEnc.objects.filter(id = compra_id).first()
	if enc:
		detalle = CompraDet.objects.filter(compra_id = compra_id)
	else:
		detalle = ""

	context = {
		"detalle": detalle,
		"enc": enc,
		"today": today,
		"request": request
	}

	# Create a Django response object, and specify content_type as pdf
	response = HttpResponse(content_type = "application/pdf")
	response["Content-Disposition"] = "inline; filename='todas_compras.pdf'"
	template = get_template(template_path)
	html = template.render(context)

	# create a pdf
	pisaStatus = pisa.CreatePDF(
		html, dest = response, link_callback = link_callback
	)
	# if error then show some funy view
	if pisaStatus.err:
		return HttpResponse("We had some errors <pre>"+ html +"</pre>")
	return response