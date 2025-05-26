
# comment generer une backup 
```
mkdir -p ~/gophish_backup/data
docker cp gophish:/opt/gophish/gophish.db ~/gophish_backup/data/gophish.db
```
# Ajouter un .env.odoo dans /gophish
  structure :
```
ODOO_EMAIL='email@trans4europe.com'
ODOO_PASSWORD='STRONG_PASSWORD'
ODOO_DB_NAME='DB8NAME'
ODOO_PORT='INT'
ODOO_HOST='HOST_DOMAINE'
```

# Maintenance

## Pour la generation de fichier de backup db 
```text
docker ps 
docker cp gophish_ID:/opt/gophish/gophish.db ./backup_gophish.db
```

## Pour la restoratin 
```text
docker cp backup_gophish.db gophish:/opt/gophish/gophish.db
```

## Redemarage
```text
docker restart gophish
```

