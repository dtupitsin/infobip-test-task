# Tasks

## 1. Ansible

Create a Ansible's playbook which using Ansible's role underhood to deploy Cassandra cluster with 3-5 nodes. 
Please choose one parameter from main Cassandra configuration file and make it changeable over Ansible's vars
technology. You can use Docker, VMs or real servers for Cassandra nodes.

```shell
ansible-playbook -i hosts playbooks/cassandra.yaml -DK
```
В `roles/cassandra/defaults/main.yml` доступные переменные для изменений

## 2. SQL

Create a table with few columns like Name and Surname. Put there ~10 rows with 24 hours life time per each row. 
Try to select data from this table by one of surnames. All queries have to be executed with strong consistency level.
It would be nice  to see a report about your performed steps with code if you decide to write a script or small 
app for that. 

Для воспроизведения действий написан python скрипт `run.py`. 

Для запуска скрипта нужно установить библиотеку для работы с cassandra:
```shell
python3 -m venv venv
. venv/bin/activate.sh
pip install -r requirements.txt
```

В консоли для установки уровня целостности высталяем `CONSISTENCY QUORUM`, в скрипте использую ExecutionProfile, с выставленным уровнем `ConsistencyLevel.LOCAL_QUORUM`

```sql
    CREATE TABLE IF NOT EXISTS users (
        id UUID primary key,
        name varchar,
        surname varchar
    );
```
и вспомогательный индекс по фамилии, он не обязателен, но позволит не писать `ALLOW FILTERING` 
```sql
CREATE INDEX IF NOT EXISTS users_surname_idx ON users (surname);
```

далее можно наполнить данными
```sql
INSERT INTO users (id, name, surname) VALUES (uuid(), 'Ivan', 'Ivanov') USING TTL 86400;
```

```sql
SELECT * FROM users WHERE surname = 'Ivanov';
```