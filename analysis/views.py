# csv_analysis/views.py

from django.shortcuts import render
import pandas as pd
import numpy as np
from .forms import UploadFileForm
import matplotlib.pyplot as plt
import seaborn as sns
import os

def home(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            df = pd.read_csv(file)
            
            # Basic data analysis
            summary_stats = df.describe().to_html()
            first_few_rows = df.head().to_html()

            # Handling missing values
            missing_values = df.isnull().sum().to_frame(name='Missing Values')

            # Calculate median for numerical columns
            medians = df.median(numeric_only=True).to_frame(name='Median').to_html()

            # Data visualization
            plt.figure(figsize=(10, 6))
            numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
            if numeric_columns:
                sns.histplot(df[numeric_columns[0]], bins=20)
                plt.title(f'Histogram of {numeric_columns[0]}')
                plt.xlabel('Value')
                plt.ylabel('Frequency')
                plt.tight_layout()

                # Save the plot to a file
                if not os.path.exists('csv_analysis/static'):
                    os.makedirs('csv_analysis/static')
                histogram_img = 'histogram.png'
                plt.savefig(f'csv_analysis/static/{histogram_img}')
                plt.close()

                return render(request, 'csv_analysis/home.html', {
                    'form': form,
                    'summary_stats': summary_stats,
                    'first_few_rows': first_few_rows,
                    'missing_values': missing_values.to_html(),
                    'medians': medians,
                    'histogram_img': histogram_img,
                })
            else:
                return render(request, 'csv_analysis/home.html', {
                    'form': form,
                    'summary_stats': summary_stats,
                    'first_few_rows': first_few_rows,
                    'missing_values': missing_values.to_html(),
                    'medians': medians,
                    'histogram_img': None,
                })
    else:
        form = UploadFileForm()
    
    return render(request, 'csv_analysis/home.html', {'form': form})
