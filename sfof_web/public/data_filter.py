import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib import utils
# Read the CSV file
def gen_doc():

    matplotlib.use('Agg')
    df = pd.read_csv('filtered_data.csv')
# Remove outliers using the IQR method
    Q1 = df.quantile(0.1)
    Q3 = df.quantile(0.9)
    IQR = Q3 - Q1
    outliers = ((df < (Q1 - 1.5 * IQR)) | (df > (Q3 + 1.5 * IQR))).any(axis=1)
    outlier_count = outliers.sum()
    outlier_percentage = outlier_count / len(df) * 100
    df_clean = df[~outliers]

# Calculate statistical description for each group
# stat_desc = df_clean.groupby('name')[['l', 'w', 'h']].describe()
    grouped_data = df.groupby('name')

# Calculate the statistical descriptions for each group
    stats = grouped_data[['l', 'w', 'h']].describe()
# Plot 3D trajectory
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    colors_dict = {'Car': 'blue', 'Truck': 'red', 'Bus': 'green', 'Pedestrian': 'orange', 'Cyclist': 'purple'}

    for name, group in df_clean.groupby('name'):
        ax.plot(group['cx'], group['cy'], group['cz'], color=colors_dict[name], label=name, marker='o')

    ax.set_xlabel('cx')
    ax.set_ylabel('cy')
    ax.set_zlabel('cz')
    ax.legend()
    plt.savefig("3D_trajectory.png")

    for name, group in df_clean.groupby('name'):
        ax.plot(group['l'], group['w'], group['h'], color=colors_dict[name], label=name, marker='o')
    ax.set_xlabel('l')
    ax.set_ylabel('w')
    ax.set_zlabel('h')
    ax.legend()
    plt.savefig("3D_whl.png")
# Plot bar plots for l, w, and h
    for col in ['l', 'w', 'h','cx','cy','cz']:
        plt.figure()
        sns.histplot(data=df_clean, x=col, hue='name', palette=colors_dict, bins=20)
        plt.title(f'Distribution of {col}')
        plt.savefig(f"{col}_distribution.png")

# Create PDF report
    doc = SimpleDocTemplate("Data Screening Technical Report.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    title = Paragraph("Data Screening Technical Report", styles['Heading1'])
    story.append(title)
    story.append(Spacer(1, 20))


    title = Paragraph("Remove Outliers Using the IQR Method", styles['Heading2'])

    story.append(title)
    outlier_info = Paragraph(f"Outliers: {outlier_count} ({outlier_percentage:.2f}% of total data)", styles['BodyText'])
    story.append(outlier_info)
# story.append(Spacer(1, 10))

# Create a formatted table


    title = Paragraph("Statistical Descriptions of l, w, and h by Object Type", styles['Heading2'])
    story.append(title)
    table_data = [['', 'Count', 'Mean', 'Std', 'Min', '25%', '50%', '75%', 'Max']]
    for name, group in stats.iterrows():
        for stat in ['l', 'w', 'h']:
            row = [f'{name} ({stat})'] + list(group[stat].round(2))
            table_data.append(row)
    table = Table(table_data)

# Apply the table style
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.black),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])

    table.setStyle(table_style)

# Alternate row colors
    row_number = len(table_data)
    for i in range(1, row_number):
        if i % 2 == 0:
            bc = colors.white
        else:
            bc = colors.white
        ts = TableStyle([('BACKGROUND', (0, i), (-1, i), bc)])
        table.setStyle(ts)
    story.append(table)

# Create a formatted table for each object type

    description = Paragraph(
        "The table above displays the statistical description of length (l), width (w), and height (h) for each object type. The following images (3D trajectory and histograms) provide a visual representation of the data.", styles['BodyText'])
    story.append(description)
    story.append(Spacer(1, 10))

    def create_image_table():
        img_paths = [
            ["3D_trajectory.png", "l_distribution.png"],
            ["w_distribution.png", "h_distribution.png"],
            ["3D_whl.png", "cx_distribution.png"],
            ["cy_distribution.png", "cz_distribution.png"]
        ]

        table_data = [[Image(path, width=240, height=180) for path in row] for row in img_paths]

        image_table = Table(table_data, colWidths=240, rowHeights=180)
        image_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER')
        ]))

        return image_table

# Add the image table to the story
    image_table = create_image_table()
    story.append(image_table)
    conclusion = Paragraph("This report provides an overview of the dataset after outlier removal, including statistical descriptions and visualizations of key features. The information presented can be valuable for further data analysis, modeling, and decision-making.", styles['BodyText'])
    story.append(conclusion)
    doc.build(story)

