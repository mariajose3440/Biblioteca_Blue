#!/bin/bash
# Espera a que el nodo primario esté listo, inicia el replica set
# y crea el usuario que usa mongoengine en settings.py.

set -e

echo "Esperando a que biblioteca_blue:27018 responda..."
until mongosh --host biblioteca_blue --port 27018 --eval "db.adminCommand('ping')" > /dev/null 2>&1; do
  sleep 2
done

echo "Iniciando replica set rs0..."
mongosh --host biblioteca_blue --port 27018 <<EOF
rs.initiate({
  _id: "rs0",
  members: [
    { _id: 0, host: "biblioteca_blue:27018" },
    { _id: 1, host: "replica_biblioteca_blue:27019" },
    { _id: 2, host: "replica_biblioteca_blue2:27020" }
  ]
});
EOF

echo "Esperando a que se elija un PRIMARY..."
until mongosh --host biblioteca_blue --port 27018 --quiet --eval "rs.isMaster().ismaster" | grep -q true; do
  sleep 2
done

echo "Creando usuario bluebul_user..."
mongosh --host biblioteca_blue --port 27018 <<EOF
db = db.getSiblingDB("biblioteca_blue");
if (db.getUser("bluebul_user") == null) {
  db.createUser({
    user: "bluebul_user",
    pwd: "webapp123seguro",
    roles: [ { role: "readWrite", db: "biblioteca_blue" } ]
  });
  print("Usuario creado.");
} else {
  print("El usuario ya existía, no se hizo nada.");
}
EOF

echo "Mongo replica set listo."
