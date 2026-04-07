"""
Automatic Database Setup Script
Handles database, user, and table creation for any environment
Run once: python setup_database.py
"""

import os
import sys
from pathlib import Path
import logging
from urllib.parse import urlparse

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    import pymysql
    from sqlmodel import SQLModel, create_engine, Session, select
    from sqlalchemy.exc import OperationalError, ProgrammingError
    from dotenv import load_dotenv
except ImportError as e:
    logger.error(f"Missing required package: {e}")
    logger.error("Run: pip install -r backend/requirements.txt")
    sys.exit(1)

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    logger.error("DATABASE_URL not set in .env file")
    logger.error("Copy .env.example to .env and configure it")
    sys.exit(1)

# Parse database URL
try:
    parsed_url = urlparse(DATABASE_URL)
    db_user = parsed_url.username
    db_password = parsed_url.password
    db_host = parsed_url.hostname
    db_port = parsed_url.port or 3306
    db_name = parsed_url.path.strip('/')
except Exception as e:
    logger.error(f"Invalid DATABASE_URL format: {e}")
    sys.exit(1)

logger.info(f"Database Configuration:")
logger.info(f"  Host: {db_host}")
logger.info(f"  Port: {db_port}")
logger.info(f"  Database: {db_name}")
logger.info(f"  User: {db_user}")


def create_database_and_user():
    """Create database and user if they don't exist"""
    logger.info("\n" + "="*60)
    logger.info("STEP 1: Creating Database and User")
    logger.info("="*60)
    
    try:
        # Connect to MySQL root (assuming default/no password for root)
        # If root has password, update below
        root_connection = pymysql.connect(
            host=db_host,
            port=db_port,
            user='root',
            password=os.getenv('DATABASE_ROOT_PASS', ''),
            charset='utf8mb4'
        )
        logger.info("✓ Connected to MySQL as root")
    except pymysql.err.OperationalError as e:
        logger.error(f"✗ Could not connect to MySQL as root")
        logger.error(f"  Error: {e}")
        logger.error(f"  Ensure MySQL is running and root password is correct")
        logger.error(f"  To set root password in .env: DATABASE_ROOT_PASS=your_password")
        raise
    
    cursor = root_connection.cursor()
    
    try:
        # Create database
        logger.info(f"Creating database '{db_name}'...")
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS `{db_name}` "
            f"CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        root_connection.commit()
        logger.info(f"✓ Database '{db_name}' created/verified")
        
        # Create user if not exists
        logger.info(f"Creating user '{db_user}'@'{db_host}'...")
        
        # First try to drop user if exists (to recreate with new password)
        try:
            cursor.execute(f"DROP USER IF EXISTS '{db_user}'@'{db_host}'")
            root_connection.commit()
            logger.info(f"  Existing user dropped")
        except Exception as e:
            logger.debug(f"  Could not drop user: {e}")
            pass
        
        # Create user
        cursor.execute(
            f"CREATE USER '{db_user}'@'{db_host}' IDENTIFIED BY '{db_password}'"
        )
        root_connection.commit()
        logger.info(f"✓ User '{db_user}' created")
        
        # Grant privileges
        logger.info(f"Granting privileges...")
        cursor.execute(
            f"GRANT ALL PRIVILEGES ON `{db_name}`.* TO '{db_user}'@'{db_host}'"
        )
        cursor.execute("FLUSH PRIVILEGES")
        root_connection.commit()
        logger.info(f"✓ Privileges granted")
        
    except pymysql.err.ProgrammingError as e:
        if "already exists" in str(e):
            logger.info(f"✓ User/database already exists: {e}")
        else:
            logger.error(f"✗ Database operation failed: {e}")
            raise
    finally:
        cursor.close()
        root_connection.close()
    
    logger.info("✓ Database and user setup complete\n")


def create_tables():
    """Create tables using SQLModel"""
    logger.info("="*60)
    logger.info("STEP 2: Creating Tables")
    logger.info("="*60)
    
    try:
        # Import models
        from app.models import Farmer, Plot
        
        # Create engine
        engine = create_engine(
            DATABASE_URL,
            echo=False,
            pool_pre_ping=True
        )
        
        # Create tables
        logger.info(f"Creating tables from models...")
        SQLModel.metadata.create_all(engine)
        logger.info(f"✓ Tables created successfully")
        
        # Verify tables exist
        logger.info(f"Verifying tables...")
        with Session(engine) as session:
            # Try to query each table
            try:
                session.exec(select(Farmer)).all()
                logger.info(f"✓ Farmer table verified")
                session.exec(select(Plot)).all()
                logger.info(f"✓ Plot table verified")
            except Exception as e:
                logger.error(f"✗ Table verification failed: {e}")
                raise
        
        logger.info("✓ All tables created and verified\n")
        return engine
        
    except Exception as e:
        logger.error(f"✗ Failed to create tables: {e}")
        raise


def seed_sample_data(engine):
    """Optionally seed sample data"""
    logger.info("="*60)
    logger.info("STEP 3: Sample Data (Optional)")
    logger.info("="*60)
    
    try:
        from app.models import Farmer, Plot
        
        with Session(engine) as session:
            # Check if data already exists
            existing_farmers = session.exec(select(Farmer)).first()
            
            if existing_farmers:
                logger.info("✓ Sample data already exists, skipping...")
                logger.info("✓ Database setup complete!\n")
                return
            
            # Ask user if they want to seed
            response = input("Add sample data? (y/n): ").lower().strip()
            
            if response != 'y':
                logger.info("✓ Skipping sample data\n")
                return
            
            # Create sample farmer
            logger.info("Adding sample farmer...")
            farmer = Farmer(
                name="Ram Kumar",
                phone="+919876543210",
                language="mr"
            )
            session.add(farmer)
            session.commit()
            session.refresh(farmer)
            logger.info(f"✓ Created farmer: {farmer.name} (ID: {farmer.id})")
            
            # Create sample plots
            plots_data = [
                {"name": "North Field", "crop": "tomato", "area_hectares": 1.5},
                {"name": "South Field", "crop": "pepper", "area_hectares": 2.0},
                {"name": "West Plot", "crop": "onion", "area_hectares": 0.8},
            ]
            
            logger.info("Adding sample plots...")
            for plot_data in plots_data:
                plot = Plot(
                    name=plot_data["name"],
                    crop=plot_data["crop"],
                    area_hectares=plot_data["area_hectares"],
                    farmer_id=farmer.id
                )
                session.add(plot)
                session.commit()
                session.refresh(plot)
                logger.info(f"✓ Created plot: {plot.name} ({plot.crop})")
            
            logger.info("✓ Sample data added successfully!\n")
            
    except Exception as e:
        logger.error(f"✗ Failed to seed data: {e}")
        logger.info("You can continue without sample data\n")


def verify_connection():
    """Verify database connection works"""
    logger.info("="*60)
    logger.info("STEP 4: Verifying Connection")
    logger.info("="*60)
    
    try:
        engine = create_engine(
            DATABASE_URL,
            echo=False,
            pool_pre_ping=True
        )
        
        # Test connection
        with Session(engine) as session:
            session.exec(select(1))
        
        logger.info("✓ Database connection verified\n")
        return True
        
    except Exception as e:
        logger.error(f"✗ Connection verification failed: {e}")
        return False


def main():
    """Main setup flow"""
    logger.info("\n")
    logger.info("╔" + "="*58 + "╗")
    logger.info("║" + " AGRI ADVISORY DATABASE SETUP ".center(58) + "║")
    logger.info("╚" + "="*58 + "╝\n")
    
    try:
        # Step 1: Create database and user
        create_database_and_user()
        
        # Step 2: Create tables
        engine = create_tables()
        
        # Step 3: Seed sample data
        seed_sample_data(engine)
        
        # Step 4: Verify connection
        if verify_connection():
            logger.info("╔" + "="*58 + "╗")
            logger.info("║" + " ✓ SETUP COMPLETE! ".center(58) + "║")
            logger.info("║" + " ".center(58) + "║")
            logger.info("║" + " Next steps:".ljust(58) + "║")
            logger.info("║" + "   1. Start backend: python -m uvicorn app.main:app --reload".ljust(58) + "║")
            logger.info("║" + "   2. Start frontend: npm run dev (in frontend folder)".ljust(58) + "║")
            logger.info("║" + "   3. Open http://localhost:5173".ljust(58) + "║")
            logger.info("║" + " ".center(58) + "║")
            logger.info("╚" + "="*58 + "╝\n")
            return 0
        else:
            logger.error("Setup completed but connection verification failed")
            return 1
            
    except Exception as e:
        logger.error("\n" + "="*60)
        logger.error("✗ SETUP FAILED")
        logger.error("="*60)
        logger.error(f"Error: {e}")
        logger.error("\nTroubleshooting:")
        logger.error("  1. Ensure MySQL is running")
        logger.error("  2. Check DATABASE_URL in .env file")
        logger.error("  3. Verify DATABASE_ROOT_PASS is correct (if set)")
        logger.error("  4. Check 'SETUP.md' for detailed instructions")
        logger.error("="*60 + "\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
