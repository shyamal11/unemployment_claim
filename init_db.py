from database import Base, engine, init_db
from database.models import FraudPattern, EligibilityRule, Applicant, ClaimHistory
from database import SessionLocal
import numpy as np
from datetime import datetime, timedelta
import random
import json

def populate_db():
    # Drop all existing tables
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("Tables dropped.")

    # Create tables
    print("Creating all tables...")
    init_db()
    print("Tables created.")
    
    with SessionLocal() as db:
        print("Inserting initial data...")
        # ======================
        # 1. Enhanced Fraud Patterns
        # ======================
        fraud_patterns = [
            {
                "description": "Fake termination letter with forged signatures", 
                "severity": 4,
                "embedding": [random.uniform(0.7, 0.9) for _ in range(768)]  # High values for forgery
            },
            {
                "description": "Employer-employee collusion (shell companies)",
                "severity": 5,
                "embedding": [random.uniform(0.6, 0.8) for _ in range(768)]
            },
            {
                "description": "Earnings inflation (reporting fake overtime)",
                "severity": 3,
                "embedding": [random.uniform(0.5, 0.7) for _ in range(768)]
            },
            {
                "description": "Duplicate claims across state lines",
                "severity": 4,
                "embedding": [random.uniform(0.8, 1.0) for _ in range(768)]
            },
            {
                "description": "Fabricated harassment allegations",
                "severity": 4,
                "embedding": [random.uniform(0.6, 0.9) for _ in range(768)]
            },
            {
                "description": "Misclassified independent contractors",
                "severity": 3,
                "embedding": [random.uniform(0.4, 0.6) for _ in range(768)]
            }
        ]
        
        for pattern in fraud_patterns:
            db.add(FraudPattern(
                description=pattern["description"],
                embedding=pattern["embedding"],
                severity=pattern["severity"]
            ))
        
        # ======================
        # 2. Eligibility Rules
        # ======================
        rules = [
            {
                "rule_name": "min_employment",
                "condition": "employment_months >= 6",
                "message": "Minimum 6 months employment required"
            },
            {
                "rule_name": "min_earnings",
                "condition": "earnings >= 3000",
                "message": "Minimum $3,000 earnings in base period"
            },
            {
                "rule_name": "voluntary_quit",
                "condition": "'quit' in separation_reason.lower() or 'resigned' in separation_reason.lower()",
                "message": "Voluntary separations not eligible"
            },
            {
                "rule_name": "employer_blacklist",
                "condition": "employer not in ['Fake Corp', 'Fraud LLC', 'Shell Co', 'Quick Temp']",
                "message": "Employer verification failed"
            },
            {
                "rule_name": "excessive_earnings",
                "condition": "earnings <= 15000",
                "message": "Earnings exceed reasonable threshold"
            }
        ]
        
        for rule in rules:
            db.add(EligibilityRule(
                rule_name=rule["rule_name"],
                condition=rule["condition"],
                message=rule["message"]
            ))
        
        # ======================
        # 3. Sample Claims (With Realistic Patterns)
        # ======================
        
        # Approved Claims (Legitimate)
        legit_employers = ["Acme Corp", "Globex", "Initech", "Stark Industries", "Wayne Enterprises"]
        legit_reasons = [
            "Department closure after corporate restructuring",
            "Position eliminated due to automation",
            "Company downsizing after merger",
            "End of contract (non-renewal)",
            "Business relocation"
        ]
        
        # Fraudulent Claims
        fraud_employers = ["Fake Corp", "Fraud LLC", "Shell Co", "Quick Temp", "Ghost Employer"]
        fraud_reasons = [
            "Terminated after 1 month",
            "Seasonal work ended",
            "Contract dispute",
            "Unpaid overtime",
            "Hostile work environment"
        ]
        
        # Generate sample claims
        for i in range(1, 31):
            if i <= 10:  # Fraudulent claims
                employer = random.choice(fraud_employers)
                reason = random.choice(fraud_reasons)
                earnings = random.randint(8000, 25000)  # Unusually high
                months = random.randint(1, 5)  # Short employment
                status = "denied"
                fraud_score = round(random.uniform(0.7, 1.0), 2)
                ssn = f"99{random.randint(10, 99)}"  # High-risk SSN group
            else:  # Legitimate claims
                employer = random.choice(legit_employers)
                reason = random.choice(legit_reasons)
                earnings = random.randint(3000, 12000)  # Normal range
                months = random.randint(6, 36)  # Sufficient employment
                status = "approved"
                fraud_score = round(random.uniform(0.0, 0.3), 2)
                ssn = f"10{random.randint(10, 99)}"  # Low-risk SSN group
            
            # Create embedding
            embedding = (
                [random.uniform(0.7, 0.9) for _ in range(768)] if status == "denied"
                else [random.uniform(0.1, 0.3) for _ in range(768)]
            )
            
            # Create Applicant record
            applicant = Applicant(
                ssn_last4=ssn,
                employer=employer,
                separation_reason=reason,
                separation_embedding=embedding,
                earnings=float(earnings),
                employment_months=months,
                status=status,
                fraud_score=fraud_score,
                decision_reason=f"Automated {status}: Sample {i}"
            )
            db.add(applicant)
            
            # Create ClaimHistory for temporal analysis
            if i <= 5:  # Create serial claimants (same SSN)
                for j in range(random.randint(2, 4)):
                    db.add(ClaimHistory(
                        ssn_last4=ssn,
                        employer=f"Previous Employer {j}",
                        claim_date=datetime.now() - timedelta(days=random.randint(30, 300)),
                        embedding=json.dumps([random.uniform(0.6, 0.8) for _ in range(768)])
                    ))
        
        # Special test cases
        test_cases = [
            # Extreme earnings fraud
            {
                "ssn_last4": "9999",
                "employer": "Fraud LLC",
                "separation_reason": "Terminated after 1 month",
                "earnings": 45000.0,
                "employment_months": 1,
                "status": "denied",
                "fraud_score": 0.95
            },
            # Serial claimant
            {
                "ssn_last4": "3574",
                "employer": "Quick Temp",
                "separation_reason": "Seasonal work ended",
                "earnings": 4200.0,
                "employment_months": 2,
                "status": "denied",
                "fraud_score": 0.88
            },
            # Ideal approved claim
            {
                "ssn_last4": "1001",
                "employer": "Wayne Enterprises",
                "separation_reason": "Department closure after corporate restructuring",
                "earnings": 8500.0,
                "employment_months": 18,
                "status": "approved",
                "fraud_score": 0.05
            }
        ]
        
        for case in test_cases:
            db.add(Applicant(**case))
            if case["ssn_last4"] == "3574":  # Add history for serial claimant
                for j in range(5):
                    db.add(ClaimHistory(
                        ssn_last4="3574",
                        employer=f"Temp Employer {j}",
                        claim_date=datetime.now() - timedelta(days=30*j),
                        embedding=json.dumps([random.uniform(0.6, 0.8) for _ in range(768)])
                    ))
        
        db.commit()
        print("Database initialized with enhanced sample data!")

if __name__ == "__main__":
    populate_db()