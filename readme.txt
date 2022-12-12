### create database name 'todos'
### create '.env' file

******** run command *********
# python3 -m venv env
# source env/bin/activate
# pip3 install -r requirements.txt
# cd src
# alembic upgrade head
# python3 main.py 

*********** add the following lines into .env ************
DATABASE_URL=mysql+mysqlconnector://root:@localhost:3306/todos
URL_ONE=http://localhost:3000
URL_TWO=https://localhost:300