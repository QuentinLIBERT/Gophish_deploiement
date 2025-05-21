import os
import pandas as pd
import odoorpc
import re
import config
from collections import defaultdict

def connection_to_odoo():
    print("Connexion au serveur Odoo...")
    odoo = odoorpc.ODOO(config.ODOO_HOST, protocol='jsonrpc+ssl', port=config.ODOO_PORT)
    odoo.login(config.ODOO_DB, config.ODOO_EMAIL, config.ODOO_PASSWORD)
    print("✅ Connecté à Odoo")
    return odoo


def clean_name(name):
    if not name:
        return ""
    return re.sub(r'\s*\(.*?\)', '', name).strip()


def afficher_champs_employes():
    odoo = connection_to_odoo()
    try:
        Employe = odoo.env['hr.employee']
        champs = Employe.fields_get()
        print(f"\n📋 Champs du modèle 'hr.employee':\n")
        for nom, definition in champs.items():
            print(f"- {nom} ({definition['type']}) - {definition.get('string', '')}")
    except Exception as e:
        print(f"❌ Erreur : {e}")



def split_display_name(display_name):
    """Sépare display_name en first_name / last_name"""
    parts = display_name.strip().split(" ", 1)
    first_name = parts[0]
    last_name = parts[1] if len(parts) > 1 else ''
    return first_name, last_name

def exporter_employes_par_departement(output_dir="export_employes"):
    odoo = connection_to_odoo()
    Employee = odoo.env['hr.employee']

    fields = ['display_name', 'work_email', 'department_id', 'job_title']
    employees = Employee.search_read([], fields)

    grouped = defaultdict(list)
    for emp in employees:
        display_name = str(emp.get("display_name") or "").strip()
        email = str(emp.get("work_email") or "").strip()
        dept_info = emp.get("department_id", [])
        full_department = dept_info[1] if dept_info else "Sans Département"
        department = full_department.split("/")[-1].strip()
        job_title = str(emp.get("job_title") or "").strip()

        first_name, last_name = split_display_name(display_name)

        grouped[department].append({
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "departement": department,
            "position": job_title
        })

    os.makedirs(output_dir, exist_ok=True)

    for dept, employes in grouped.items():
        file_name = dept.replace(" ", "_").replace("/", "_")
        path = os.path.join(output_dir, f"{file_name}.csv")
        df = pd.DataFrame(employes)
        df.to_csv(path, index=False, encoding="utf-8")
        print(f"📁 Fichier généré : {path}")


if __name__ == "__main__":
    exporter_employes_par_departement()
#    afficher_champs_employes()