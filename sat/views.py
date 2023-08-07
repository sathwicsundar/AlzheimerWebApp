from django.shortcuts import render
from .models import Question
import numpy as np
from PIL import Image
from keras.models import load_model
from skimage.exposure import equalize_adapthist as eq_hist

# Create your views here.

def index(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        if image:
            my_model = Question()
            my_model.image = image
            my_model.save()

            # Call the function from the other file
            image_path = my_model.image.path
            print(image_path)
            snapshot_file = 'sat/snapshot_5.hdf5'
            loaded_model = load_model(snapshot_file)

            # Load and preprocess the image
            IMAGE_SIZE = 176

            def preprocess_image(image_path):
                im = Image.open(image_path).convert('L')
                im = im.resize((IMAGE_SIZE, IMAGE_SIZE))
                im = eq_hist(np.array(im), clip_limit=0.03)
                im = im.reshape((1, IMAGE_SIZE, IMAGE_SIZE, 1))
                return im

            preprocessed_image = preprocess_image(image_path)

            # Make predictions using the loaded model
            class_names = [
                'NonDemented',
                'VeryMildDemented',
                'MildDemented',
                'ModerateDemented',
            ]

            predictions = loaded_model.predict(preprocessed_image)
            predicted_class_index = np.argmax(predictions)
            predicted_class_name = class_names[predicted_class_index]

            print(f"The model predicts the input image belongs to the class: {predicted_class_name}")

        return render(request,'sat/res.html' , {'res' : predicted_class_name})






    return render(request,'sat/index.html')

def result(request):
    return render(request,'sat/res.html')