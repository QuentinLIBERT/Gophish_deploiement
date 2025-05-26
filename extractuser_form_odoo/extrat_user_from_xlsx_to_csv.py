import pandas as pd
import os

def export_par_email_type_et_service(input_file="utilisateurs.csv", export_dir="exports"):
    # Dossiers de sortie
    os.makedirs(export_dir, exist_ok=True)
    group_email_dir = os.path.join(export_dir, "group_emails")
    os.makedirs(group_email_dir, exist_ok=True)

    try:
        # Lire le fichier CSV avec ; et traiter "--" comme NaN
        df = pd.read_csv(input_file, sep=";", na_values="--")

        # Colonnes utiles
        output_columns = ["first_name", "last_name", "email", "service_name"]

        # Supprimer lignes incomplètes
        df.dropna(subset=["email", "email_type", "service_name"], inplace=True)

        # === Export par email_type ===
        for email_type, group in df.groupby("email_type"):
            filename = f"{email_type.lower().strip().replace(' ', '_')}.csv"
            path = os.path.join(export_dir, filename)
            group[output_columns].to_csv(path, sep=",", index=False, encoding="utf-8")
            print(f"✅ Exporté par email_type : {path}")

        # === Export par service_name ===
        for service_name, group in df.groupby("service_name"):
            filename = f"{service_name.lower().strip().replace(' ', '_').replace('/', '_')}.csv"
            path = os.path.join(export_dir, filename)
            group[output_columns].to_csv(path, sep=",", index=False, encoding="utf-8")
            print(f"✅ Exporté par service_name : {path}")

        # === Fichiers individuels group/group
        filtre_group = df[
            (df["email_type"].str.lower() == "group") &
            (df["service_name"].str.lower() == "group")
        ]

        for _, row in filtre_group.iterrows():
            email = row["email"]
            safe_email = email.lower().replace("@", "_at_").replace(".", "_")
            path = os.path.join(group_email_dir, f"group_{safe_email}.csv")

            output_row = {
                "first_name": row.get("first_name", ""),
                "last_name": row.get("last_name", ""),
                "email": row.get("email", ""),
                "service_name": row.get("service_name", "")
            }

            pd.DataFrame([output_row])[output_columns].to_csv(path, sep=",", index=False, encoding="utf-8")
            print(f"📤 Exporté fichier individuel : {path}")

    except Exception as e:
        print(f"❌ Erreur : {e}")

if __name__ == "__main__":
    export_par_email_type_et_service()
