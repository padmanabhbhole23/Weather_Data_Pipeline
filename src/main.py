from src.database import setup_database
from src.etl_pipeline import run_etl
from src.config import DEFAULT_CITIES
from src.reporter import generate_daily_report

def run_once():
    setup_database()
    result = run_etl(DEFAULT_CITIES)

    print("\nWEATHER DATA PIPELINE SYSTEM")
    print("=" * 40)
    print("📊 Run Summary:", result)

    rows, alerts = generate_daily_report()

    print("\n🌤️ Latest Weather Records:")
    for r in rows:
        print("📍", r)

    print("\n📅 ALERTS:")
    if alerts:
        for a in alerts:
            print("•", a)
    else:
        print("• None")

if __name__ == "__main__":
    run_once()
