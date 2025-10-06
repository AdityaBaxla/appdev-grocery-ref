if vscode is not giving automplete for methods, restart "python language server"

pathe error running script
(.venv) ➜  backend git:(main) ✗ python3 -m scripts.init_db   

time aware datetime.now(timezone.utc)

------------------------------
Yes! You **can leverage Flask-Security-Too** to do most of this without writing JWT from scratch. It already supports **token authentication** via `user.get_auth_token()` and can integrate with **stateless (token) auth**. I’ll show you a minimal example for both **logout/denylist** and **token-based login** using Flask-Security-Too.

---

## 1️⃣ **Setup**

```python
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from flask_security.utils import hash_password, verify_password

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_PASSWORD_SALT'] = 'salt'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = 'Authorization'

db = SQLAlchemy(app)
```

---

## 2️⃣ **Models**

```python
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users, backref='users')
```

---

## 3️⃣ **Flask-Security Setup**

```python
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
```

---

## 4️⃣ **Login Route Using Flask-Security Token**

```python
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not verify_password(password, user.password):
        return jsonify({"msg": "Invalid credentials"}), 401

    token = user.get_auth_token()  # Stateless token
    return jsonify({"token": token, "email": user.email}), 200
```

---

## 5️⃣ **Protected Route**

```python
from flask_security.decorators import auth_token_required

@app.route("/private")
@auth_token_required
def private():
    return jsonify({"msg": "Access granted"}), 200
```

* `@auth_token_required` ensures the client sends `Authorization: <token>` in the header.
* Flask-Security handles verifying the token.

---

## 6️⃣ **Logout / Denylist**

Flask-Security doesn’t have built-in token revocation for `get_auth_token()`, because it’s **stateless**.
To support “logout”, you need a **denylist table**:

```python
from datetime import datetime

class RevokedToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(512), unique=True)
    revoked_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route("/logout", methods=["POST"])
@auth_token_required
def logout():
    token = request.headers.get("Authorization")
    db.session.add(RevokedToken(token=token))
    db.session.commit()
    return jsonify({"msg": "Token revoked"}), 200
```

And then check it in a **custom token validator**:

```python
from flask_security.signals import verify_token

@verify_token.connect_via(app)
def check_revoked_token(sender, token, **extra):
    if RevokedToken.query.filter_by(token=token).first():
        return False  # token revoked
    return True
```

---

### ✅ Key Points

* **Login:** `user.get_auth_token()` → stateless token, no DB lookup every request.
* **Protected routes:** `@auth_token_required` → checks token validity.
* **Logout:** optional denylist to immediately revoke tokens.
* **Refresh tokens:** Flask-Security doesn’t provide refresh tokens by default; you’d need to implement that separately if desired.

----------------------------------------------------




Resource/Controller : validated data coming from client, authorization, authentication, http concerns (codes), Data Transformation (Serialization/Deserialization), Orchestration of service, handle query parameters
```Controllers should never contain business rules, just orchestrate them.```

Service: Data integrity, Storing and interacting with db, Validate Business Rules (user can create only one account, only 5 books can be borrowed), External Integrations
```Keep services completely unaware of HTTP or Flask; they should work even if called from a CLI script or a background job.```

Added a new step