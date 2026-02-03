import os
import zipfile

def generate_moral_compass_zip():
    project_name = 'moral_compass_ai'
    zip_name = 'moral_compass_ai_deployable.zip'
    subdirs = ['backend', 'frontend', 'data', 'admin', 'docs']

    # Create project and subdirectories
    os.makedirs(project_name, exist_ok=True)
    for folder in subdirs:
        os.makedirs(os.path.join(project_name, folder), exist_ok=True)

    # Generate questions.csv with 120 entries
    csv_path = os.path.join(project_name, 'data', 'questions.csv')
    headers = "id,category,age_group,question_en,question_bn,question_hi,question_jp,question_cn,options\n"
    categories = ["Ethics", "Social", "Professional", "Personal"]
    age_groups = ["Child", "Teen", "Adult", "Senior"]
    options = '"Always, Often, Sometimes, Rarely, Never"'

    with open(csv_path, 'w', encoding='utf-8') as f:
        f.write(headers)
        for i in range(1, 121):
            cat = categories[i % 4]
            age = age_groups[i % 4]
            row = f'{i},{cat},{age},Question EN {i},Question BN {i},Question HI {i},Question JP {i},Question CN {i},{options}\n'
            f.write(row)

    # Create dummy files for empty directories to ensure they are included in zip
    for folder in subdirs:
        if folder != 'data':
            with open(os.path.join(project_name, folder, '.gitkeep'), 'w') as f:
                f.write('')    # Package into ZIP
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(project_name):
            for file in files:
                full_path = os.path.join(root, file)
                # Maintain relative structure inside the ZIP
                archive_name = os.path.relpath(full_path, os.path.join(project_name, '..'))
                zipf.write(full_path, archive_name)

    print(f"✅ Created folder structure: {project_name}/")
    print(f"✅ Generated 120 questions: {csv_path}")
    print(f"✅ Generated deployable package: {zip_name}")

if __name__ == "__main__":
    generate_moral_compass_zip()