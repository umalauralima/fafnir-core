#!/bin/bash

# Verifica se passou nome da entidade
if [ -z "$1" ]; then
  echo "Uso: ./generate_module.sh nome_da_entidade"
  exit 1
fi

NAME=$1
CLASS_NAME="$(tr '[:lower:]' '[:upper:]' <<< ${NAME:0:1})${NAME:1}"

# Caminhos
BASE_DIR="app"
DTO_DIR="$BASE_DIR/dto"
REPO_DIR="$BASE_DIR/repositories"
SERVICE_DIR="$BASE_DIR/services"
ROUTES_DIR="$BASE_DIR/routes"

# Arquivos
DTO_FILE="$DTO_DIR/${NAME}_dto.py"
REPO_FILE="$REPO_DIR/${NAME}_repository.py"
SERVICE_FILE="$SERVICE_DIR/${NAME}_service.py"
ROUTES_FILE="$ROUTES_DIR/${NAME}_routes.py"

echo "Criando arquivos para: $NAME"

# DTO (Pydantic)
cat <<EOF > $DTO_FILE
from typing import Optional
from pydantic import BaseModel, Field


class ${CLASS_NAME}CreateDTO(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., max_length=120)


class ${CLASS_NAME}UpdateDTO(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[str] = Field(None, max_length=120)
EOF

# Repository
cat <<EOF > $REPO_FILE
class ${CLASS_NAME}Repository:
    def __init__(self, db):
        self.db = db

    def list(self):
        pass
EOF

# Service
# Service
cat <<EOF > $SERVICE_FILE
from app.repositories.${NAME}_repository import ${CLASS_NAME}Repository

class ${CLASS_NAME}Service:
    def __init__(self, db):
        self.repository = ${CLASS_NAME}Repository(db)

    def list_${NAME}s_paginated(self, page: int = 1, per_page: int = 10):
        pagination = self.repository.get_paginated(page, per_page)

        return {
            "items": pagination.items,
            "total": pagination.total,
            "page": page,
            "per_page": per_page,
            "pages": pagination.pages,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev
        }
EOF

# Routes
cat <<EOF > $ROUTES_FILE
from flask import Blueprint, jsonify
from app.services.${NAME}_service import ${CLASS_NAME}Service

${NAME}_bp = Blueprint("${NAME}", __name__)

@${NAME}_bp.route("/", methods=["GET"])
def list_${NAME}():
    service = ${CLASS_NAME}Service(db=None)  # ajustar
    result = service.list()

    return jsonify(result), 200
EOF

echo "Arquivos criados com sucesso 🚀"