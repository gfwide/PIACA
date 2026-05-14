# PIACA

## Nuvem (resumo)

Em producao, o projeto roda em uma unica EC2 publica.

- a EC2 sobe toda a stack com Docker Compose
- o Postgres roda em container na mesma EC2
- o Traefik recebe as requisicoes HTTP e roteia para os modulos
- deploy remoto e feito via AWS SSM (sem depender de SSH aberto para o pipeline)

## Arquitetura de roteamento (Traefik)

```mermaid
flowchart LR
	U[Usuario / Browser] --> T[Traefik :80]
	T --> EX[/example -> example-module]
	T --> A[/auth -> piaca-core-auth]
	T --> B[/animals -> piaca-pet-management]
	T --> C[/adoption -> piaca-adoption-ai]
	T --> D[/godparenthood -> piaca-godparenthood]
	EX --> P[(Postgres)]
	A --> P
	B --> P
	C --> P
	D --> P
```

## Como rodar

O projeto roda inteiro com um unico comando Docker Compose.

Pre-requisitos:

- Docker
- Docker Compose v2

Na raiz do repositorio:

```bash
docker volume create postgres_data (apenas uma vez)
docker compose up -d --build
```

Esse comando sobe:

- traefik
- postgres
- flyway
- frontend
- modulos habilitados no docker-compose.yml

## Variaveis de ambiente

As variaveis de banco ja tem valor default no proprio docker-compose.yml:

- DB_HOST=postgres
- DB_PORT=5432
- DB_NAME=piaca_db
- DB_USER=piaca_user
- DB_PASSWORD=piaca_pass

## Rebuild de um modulo especifico

Para rebuildar e subir so um modulo:

```bash
docker compose up -d --build <nome-do-servico>
```

Exemplo:

```bash
docker compose up -d --build example-module
```

## Comandos basicos

Ver status:

```bash
docker compose ps
```

Ver logs:

```bash
docker compose logs -f
```

Parar tudo:

```bash
docker compose down
```

## Deploy automatico (GitHub Actions + SSM)

O workflow `.github/workflows/deploy-ec2.yml` faz deploy em push na `main` via SSM.

Fluxo:

- encontra a EC2 por tag `Name` (default `piaca-ec2`)
- envia comando remoto via SSM
- na EC2 executa `git fetch/checkout` e `docker compose up -d --build`

Secrets necessarios no GitHub:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION` (exemplo: `us-east-1`)
- `EC2_APP_DIR` (opcional, default `/home/ec2-user/app`)
- `EC2_INSTANCE_TAG` (opcional, default `piaca-ec2`)

## Autores

## Grupo B: Gestao de Pets

| Aluno | Usuário do GitHub |
|-------------|---------|
| Gustavo Fulber Wide| gfwide |
| Carolina Shypelenko Kowaluk| carolina-kowaluk|
| Pietra Renner | pietrarenner|
| Gabriele Colares | gabicolares |
| Julia Agustini| juhagustinii |
| Deborah Citrin| |
| Nicolas Pietro | |
| Lucas Ulson | |

## Grupo C: Adoção e IA

| Aluno | Usuário do GitHub |
|-------------|---------|
| Heloysa Gabrielle Pelizon | heloysapelizon |
| Luiza Hackenhaar Naziazeno | luizahackenhaarnaziazeno |
| Marina Schwerz Bon | marinasbon |
| Kristen Arguello | kristenarguello |

## Grupo D: Apadrinhamento de Pets

| Aluno | Usuário do GitHub |
|-------------|---------|
| Eduardo Tomacheski Teixeira | Etomacheski |
| Gabriel Fanti de Souza | Gabriel_Fanti |
| Gustavo Rech Saul | gustavorsaul |
| João Pedro da Silva Graboski | JPG010 |
| Matheus Braun Boff | Matheus-Boff |
| Matheus Silva de Lima| MathsLima |


## Grupo E: Experiência Mobile

| Aluno | Usuário do GitHub |
|-------------|---------|
| Giordano Fraga Faccioli | giordano-fraga |
| Pedro Duarte dos Santos | PDS-Academico |
| Gabriel Andreis Pivotto | gabriel.pivotto |
| Pietro Lessa | pietrolessa |

## Grupo F: Infraestrutura e API Gateway

| Aluno | Usuário do GitHub |
|-------------|---------|
| Estevam Cabral Pacheco | estevamcabral |
| Juliano Maia | nextcoyocoatl |
| Leonardo Francisco Sehnem dos Santos | Leosehn |
| Luísa Scolari Pase | luscolari |
| Marcela Nunes Zarichta | marcelazarichta |
| Naiumy dos Reis| Naiumydosreis |
