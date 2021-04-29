from myorder_server import app
from .db import (db_acq_lock, db_rel_lock)
from flask import (jsonify)
import json
from flask import (render_template)

