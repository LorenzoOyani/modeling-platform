from app.db import RunSession
import uuid

def start_run(db, formula_id, input_file=None):
    run = RunSession(
        run_id=str(uuid.uuid4())[:8],
        formula_id=formula_id,
        input_file=input_file,
        status="RUNNING"
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    return run
