# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.core.files.base import ContentFile
from .models import Image
from rembg import remove
from PIL import Image as PILImage
import io

@login_required(login_url='login')
def remove_bg(request):
    """Remove background - images are linked to logged-in user"""
    
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_image = request.FILES['image']
        
        try:
            # ✅ Link image to the current user
            image = Image.objects.create(
                user=request.user,  # ← Add user
                original=uploaded_image
            )
            
            # Process image...
            input_img = PILImage.open(image.original.path)
            output_img = remove(input_img)
            
            img_bytes = io.BytesIO()
            output_img.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            
            image.processed.save(
                f"no_bg_{image.id}.png",
                ContentFile(img_bytes.read())
            )
            
            messages.success(request, 'Background removed successfully!')
            return redirect('result', pk=image.id)
            
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('remove_bg')
    
    return render(request, 'remove_bg.html')

@login_required(login_url='login')
def result(request, pk):
    """Show result page - only if user owns the image"""
    
    # ✅ Get image and check ownership
    image = get_object_or_404(Image, pk=pk)
    
    # 🛡️ Check if the current user owns this image
    if image.user != request.user:
        messages.error(request, "You don't have permission to view this image.")
        return redirect('remove_bg')
        # OR return HttpResponseForbidden("You don't own this image")
    
    return render(request, 'result.html', {'image': image})

@login_required(login_url='login')
def download(request, pk):
    image = get_object_or_404(Image, pk=pk)
    if image.user != request.user:
        messages.error(request, "You don't have permission to download this image.")
        return redirect('remove_bg')
    if image.processed:
        response = HttpResponse(
            image.processed.read(),
            content_type='image/png'
        )
        response['Content-Disposition'] = f'attachment; filename="no_bg_{image.id}.png"'
        return response
    
    return redirect('remove_bg')

@login_required(login_url='login')
def my_images(request):
    images = Image.objects.filter(user=request.user).order_by('-uploaded_at')
    return render(request, 'my_images.html', {'images': images})