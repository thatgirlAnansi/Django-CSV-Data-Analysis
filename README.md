# Django-CSV-Data-Analysis


Sure, here's a concise version of the guide to create a Django-based web application for uploading CSV files, performing data analysis using pandas, and displaying the results and visualizations:

### 1. Django Setup

1. **Install Django and other dependencies**:
   ```bash
   pip install django pandas matplotlib
   ```

2. **Create a Django project and app**:
   ```bash
   django-admin startproject data_analysis_project
   cd data_analysis_project
   python manage.py startapp analysis
   ```

3. **Configure the project**:
   Add 'analysis' to `INSTALLED_APPS` in `data_analysis_project/settings.py`.

### 2. File Upload Feature

1. **Create a form for file upload** (`analysis/forms.py`):
   ```python
   from django import forms

   class UploadFileForm(forms.Form):
       file = forms.FileField()
   ```

2. **Create a view to handle the upload** (`analysis/views.py`):
   ```python
   from django.shortcuts import render
   from .forms import UploadFileForm
   import pandas as pd
   import os
   from django.conf import settings
   import matplotlib.pyplot as plt

   def handle_uploaded_file(f):
       file_path = os.path.join(settings.MEDIA_ROOT, f.name)
       with open(file_path, 'wb+') as destination:
           for chunk in f.chunks():
               destination.write(chunk)
       return file_path

   def upload_file(request):
       if request.method == 'POST':
           form = UploadFileForm(request.POST, request.FILES)
           if form.is_valid():
               file_path = handle_uploaded_file(request.FILES['file'])
               df = pd.read_csv(file_path)
               return render(request, 'analysis/results.html', {'df': df.head().to_html(), 'stats': df.describe().to_html()})
       else:
           form = UploadFileForm()
       return render(request, 'analysis/upload.html', {'form': form})
   ```

3. **Create templates**:
   `analysis/templates/analysis/upload.html`:
   ```html
   <html>
   <body>
       <h1>Upload CSV File</h1>
       <form method="post" enctype="multipart/form-data">
           {% csrf_token %}
           {{ form.as_p }}
           <button type="submit">Upload</button>
       </form>
   </body>
   </html>
   ```

   `analysis/templates/analysis/results.html`:
   ```html
   <html>
   <body>
       <h1>Data Analysis Results</h1>
       <h2>Data</h2>
       {{ df|safe }}
       <h2>Summary Statistics</h2>
       {{ stats|safe }}
   </body>
   </html>
   ```

4. **Configure URLs**:
   `analysis/urls.py`:
   ```python
   from django.urls import path
   from . import views

   urlpatterns = [
       path('', views.upload_file, name='upload_file'),
   ]
   ```

   `data_analysis_project/urls.py`:
   ```python
   from django.urls import path, include

   urlpatterns = [
       path('admin/', admin.site.urls),
       path('', include('analysis.urls')),
   ]
   ```

### 3. Data Processing

Modify `upload_file` view in `analysis/views.py` to include data processing:
```python
import numpy as np

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_path = handle_uploaded_file(request.FILES['file'])
            df = pd.read_csv(file_path)
            df.fillna(df.mean(), inplace=True)
            stats = df.describe().to_html()
            histograms = []
            for column in df.select_dtypes(include=[np.number]).columns:
                plt.figure()
                df[column].hist()
                img_path = os.path.join(settings.MEDIA_ROOT, f'{column}_hist.png')
                plt.savefig(img_path)
                histograms.append(img_path)
            return render(request, 'analysis/results.html', {
                'df': df.head().to_html(),
                'stats': stats,
                'histograms': histograms,
            })
    else:
        form = UploadFileForm()
    return render(request, 'analysis/upload.html', {'form': form})
```

### 4. Data Visualization

Modify `analysis/templates/analysis/results.html` to display histograms:
```html
<html>
<body>
    <h1>Data Analysis Results</h1>
    <h2>Data</h2>
    {{ df|safe }}
    <h2>Summary Statistics</h2>
    {{ stats|safe }}
    <h2>Histograms</h2>
    {% for hist in histograms %}
        <img src="{{ hist }}" alt="Histogram">
    {% endfor %}
</body>
</html>
```

### 5. User Interface

Configure `settings.py` to serve media files:
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

Update `data_analysis_project/urls.py` to serve media files:
```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### Running the Server

1. **Apply migrations**:
   ```bash
   python manage.py migrate
   ```

2. **Run the server**:
   ```bash
   python manage.py runserver
   ```

3. **Access the application**:
   Open your web browser and go to `http://127.0.0.1:8000/`.
