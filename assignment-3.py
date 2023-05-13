import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# Read in the CSV file using pandas
data = pd.read_csv('blood_pressure_data.csv')

# Extract the age and blood pressure columns
age = data['Age']
bp = data['Blood Pressure']

# Calculate the Pearson correlation coefficient
pearson_correlation = stats.pearsonr(age, bp)[0]

# Calculate the Spearman correlation coefficient
spearman_correlation = stats.spearmanr(age, bp)[0]

# Calculate the linear regression model
slope, intercept, r_value, p_value, std_err = stats.linregress(age, bp)

# Create the regression equation
regression_equation = f"y = {slope:.2f}x + {intercept:.2f}"

# Create a table to display the correlation coefficients and regression equation
data = [['Statistic', 'Value'], ['Pearson Correlation Coefficient', pearson_correlation], ['Spearman Correlation Coefficient', spearman_correlation], ['Regression Equation', regression_equation]]
table = Table(data)
table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.darkgray),
    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,0), 14),
    ('BOTTOMPADDING', (0,0), (-1,0), 12),
    ('BACKGROUND', (0,1), (-1,-1), colors.beige),
    ('TEXTCOLOR', (0,1), (-1,-1), colors.black),
    ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
    ('FONTSIZE', (0,1), (-1,-1), 12),
    ('BOTTOMPADDING', (0,1), (-1,-1), 10),
    ('GRID', (0,0), (-1,-1), 1, colors.black)
]))

# Create a scatter plot of the age and blood pressure data with the regression line
fig, ax = plt.subplots()
ax.scatter(age, bp)
ax.plot(age, slope * age + intercept, color='red')
ax.set_xlabel('Age')
ax.set_ylabel('Blood Pressure')
ax.set_title('Age vs. Blood Pressure')
plt.savefig('scatter.png')
plt.close()

# Create a PDF report
doc = SimpleDocTemplate('report-5.pdf', pagesize=letter)
elements = []

# Add the table to the PDF report
elements.append(table)

# Add the scatter plot to the PDF report
elements.append(Image('scatter.png'))

# Add the regression equation and prediction to the PDF report
styles = getSampleStyleSheet()
text = f"The predicted blood pressure for a man aged 25 years is {slope*25+intercept:.2f} mm Hg."
elements.append(Paragraph(regression_equation, styles['Normal']))
elements.append(Paragraph(text, styles['Normal']))

doc.build(elements)
