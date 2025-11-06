from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Cria a aplicação Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'minha-chave-secreta-123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Cria o banco de dados
db = SQLAlchemy(app)

# Modelo para as tarefas
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='To Do')
    priority = db.Column(db.String(10), default='Medium')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.title}>'

# Página principal - mostra o Kanban
@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

# Criar nova tarefa
@app.route('/task', methods=['POST'])
def create_task():
    try:
        title = request.form.get('title')
        description = request.form.get('description', '')
        priority = request.form.get('priority', 'Medium')
        
        new_task = Task(
            title=title,
            description=description,
            priority=priority
        )
        
        db.session.add(new_task)
        db.session.commit()
        
        flash('✅ Tarefa criada com sucesso!', 'success')
    except Exception as e:
        flash('❌ Erro ao criar tarefa', 'error')
    
    return redirect(url_for('index'))

# Executar a aplicação
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("🎯 Servidor rodando em: http://localhost:5000")
    app.run(debug=True)