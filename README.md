# Guia prático para iniciantes em Docker e Docker Compose

## Introdução
O objetivo deste workshop é orientar os iniciantes no processo de containerização de suas aplicações usando o Docker. Ao final deste workshop, eles deverão ser capazes de containerizar seus serviços usando o Docker e executá-los localmente de maneira semelhante ao Mesos.

## Primeiros Passos
O primeiro passo é entender como criar um contêiner. Vamos começar com o Dockerfile, que serve como a receita para o nosso contêiner. As instruções mais comuns são as seguintes:

- `FROM`: Especifica a imagem base usada na construção do contêiner.
- `ENV`: Define variáveis de ambiente persistidas no contêiner.
- `RUN`: Executa comandos shell, úteis para instalar pacotes ou configurar serviços durante a construção.
- `WORKDIR`: Define o diretório para executar as instruções do Dockerfile.
- `COPY`: Copia arquivos da máquina host para o contêiner.
- `ENTRYPOINT`: Especifica o executável a ser usado quando o contêiner é executado.
- `CMD`: Define os argumentos passados para o executável.


```Dockerfile
FROM python:alpine

ENV POSTGRES_DATABASE=communication

RUN pip install flask
WORKDIR /src
COPY /src .

ENTRYPOINT [ "python3" ]
CMD [ "/src/api.py" ]
```

Depois de definir o Dockerfile, o próximo passo é construir a imagem. Uma imagem é essencialmente um conjunto comprimido de arquivos.

```bash
docker build -t basic-image:0.0.1-SNAPSHOT .
```

## Construindo e Executando Contêineres
Após construir a imagem, vamos configurar alguns parâmetros e executar nosso contêiner.

```bash
docker run --name basic-api -d -p 8001:5001 basic-image:0.0.1-SNAPSHOT
```

Para verificar se o contêiner está sendo executado corretamente e visualizar seus logs:

```bash
docker ps -a
docker logs basic-api -f
```

## Interagindo com os Contêineres
Se precisar acessar o shell do contêiner:

```bash
docker exec -it basic-api /bin/sh
```

Demonstrar a diferença entre `ENTRYPOINT` e `CMD` usando `ls` como exemplo.

## Monitorando o Desempenho dos Contêineres
Para monitorar o desempenho dos contêineres:

```bash
docker stats
```

## Simplificando o Gerenciamento de Contêineres com Docker Compose
Gerenciar contêineres via linha de comando pode ser complicado, especialmente ao lidar com vários serviços. É aí que o Docker Compose é útil. O Docker Compose simplifica a construção e execução de vários contêineres. Pense nele como semelhante ao `service.json` do Mesos.


## De service.json para docker-compose.yaml

```json
{
	"id": "service-basic-api-service",
	"cpus": 0.25,
	"instances": 1,
	"mem": 256,
	"resourceLimits": {
 		"cpus": 0.5,
 		"mem": 512
	},
	"networks": [
		{
			"mode": "container/bridge"
		}
	],
	"container": {
		"portMappings": [
			{
				"containerPort": 5001,
				"labels": {
					"VIP_0": "/service-basic-api-service:5001"
				}
			}
		],
		"type": "DOCKER",
		"volumes": [
			{
				"containerPath": "/persistent-data",
				"mode": "RW",
				"external": {
					"name": "basic-api-volume",
					"provider": "dvdi",
					"options": {
						"dvdi/driver": "rexray"
					}
				}
			}
		],
		"docker": {
			"image": "service-basic-api-service:0.0.1-SNAPSHOT",
			"forcePullImage": true
		}
	},
	"fetch": [
		{
			"uri": "file:///etc/private-docker.tar.gz"
		}
	],
	"env": {
		"POSTGRES_DATABASE": "personal-lending"
	}
}
```

Perceba que nem todas as chaves do `service.json` são necessárias no `docker-compose.yaml`.

```Dockerfile
services:
  basic-api:
    build: .
    image: basic-image:0.0.2-SNAPSHOT
    container_name: basic-api
    environment:
      - POSTGRES_DATABASE=personal-lending
    ports:
      - 8001:5001
    volumes:
      - ./src:/src
      - basic-api-volume:/persistent-data
    deploy:
      resources:
        reservations:
          cpus: "0.25"
          memory: 256M
        limits:
          cpus: "0.50"
          memory: 512M

volumes:
  basic-api-volume:
```


