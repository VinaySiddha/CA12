#!/bin/bash

# Database setup script for Intelligent Matchmaking System
# This script sets up MongoDB and populates it with sample data

echo "🚀 Setting up Intelligent Matchmaking System Database..."

# Check if MongoDB is running (Windows-compatible)
if command -v mongosh > /dev/null 2>&1; then
    # Try to connect to MongoDB to check if it's running
    if ! mongosh "mongodb://localhost:27017" --eval "db.runCommand('ping')" --quiet > /dev/null 2>&1; then
        echo "❌ MongoDB is not running. Please start MongoDB first."
        echo "   For Windows: net start MongoDB"
        echo "   For macOS: brew services start mongodb-community"
        echo "   For Linux: sudo systemctl start mongod"
        exit 1
    fi
else
    echo "❌ mongosh is not installed or not in PATH"
    echo "   Please install MongoDB and ensure mongosh is available"
    exit 1
fi

echo "✅ MongoDB is running"

# Database configuration
DB_NAME="intelligent_matchmaking"
MONGO_URI="mongodb://localhost:27017"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "📊 Database: $DB_NAME"
echo "🔗 MongoDB URI: $MONGO_URI"

# Run MongoDB setup script
echo "🔧 Creating database indexes..."
if mongosh "$MONGO_URI/$DB_NAME" --file "$SCRIPT_DIR/mongo_setup.js" --quiet; then
    echo "✅ Database indexes created successfully"
else
    echo "❌ Failed to create database indexes"
    exit 1
fi

# Step 4: Import seed data
echo "� Importing seed data..."

# Check if we're on Windows or Unix-like system
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" || "$OSTYPE" == "cygwin" ]]; then
    echo "🪟 Windows system detected - using Python import script..."
    
    # Check if Python is available
    if ! command -v python &> /dev/null; then
        echo "❌ Python is not installed. Please install Python 3.7+ and try again."
        exit 1
    fi
    
    # Install pymongo if not available
    python -c "import pymongo" 2>/dev/null || {
        echo "📦 Installing pymongo..."
        pip install pymongo
    }
    
    # Run the Python import script
    python import_seed_data.py
    
else
    # Unix-like systems - use jq and mongoimport
    echo "🐧 Unix-like system detected - using jq and mongoimport..."
    
    # Check if jq is available for JSON processing
    if ! command -v jq &> /dev/null; then
        echo "❌ jq is not installed. Installing..."
        # Install jq based on the system
        if [[ "$OSTYPE" == "linux-gnu"* ]]; then
            sudo apt-get update && sudo apt-get install -y jq
        elif [[ "$OSTYPE" == "darwin"* ]]; then
            brew install jq
        else
            echo "❌ Unable to install jq automatically. Please install jq manually."
            echo "Visit: https://stedolan.github.io/jq/download/"
            exit 1
        fi
    fi

    # Import seed data using jq and mongoimport
    echo "Importing users..."
    jq -c '.users[]' seed_data.json | mongoimport --db intelligent_matchmaking --collection users --type json

    echo "Importing study groups..."
    jq -c '.study_groups[]' seed_data.json | mongoimport --db intelligent_matchmaking --collection study_groups --type json

    echo "Importing learning resources..."
    jq -c '.learning_resources[]' seed_data.json | mongoimport --db intelligent_matchmaking --collection learning_resources --type json

    echo "Importing sessions..."
    jq -c '.sessions[]' seed_data.json | mongoimport --db intelligent_matchmaking --collection sessions --type json

    echo "Importing matches..."
    jq -c '.matches[]' seed_data.json | mongoimport --db intelligent_matchmaking --collection matches --type json

    echo "Importing feedback..."
    jq -c '.feedback[]' seed_data.json | mongoimport --db intelligent_matchmaking --collection feedback --type json

    echo "Importing gamification data..."
    jq -c '.gamification[]' seed_data.json | mongoimport --db intelligent_matchmaking --collection gamification --type json

    echo "Importing notifications..."
    jq -c '.notifications[]' seed_data.json | mongoimport --db intelligent_matchmaking --collection notifications --type json
fi
done

echo ""
echo "🎉 Database setup completed successfully!"
echo ""
echo "📈 Database Statistics:"

# Get database stats
mongosh "$MONGO_URI/$DB_NAME" --eval "
    print('Database: ' + db.getName());
    print('Collections: ' + db.runCommand('listCollections').cursor.firstBatch.length);
    
    var collections = db.runCommand('listCollections').cursor.firstBatch;
    var totalDocs = 0;
    
    collections.forEach(function(collection) {
        var count = db.getCollection(collection.name).countDocuments();
        if (count > 0) {
            print('  - ' + collection.name + ': ' + count + ' documents');
            totalDocs += count;
        }
    });
    
    print('Total documents: ' + totalDocs);
" --quiet

echo ""
echo "🔗 Next steps:"
echo "   1. Start the FastAPI backend: cd backend && uvicorn app.main:app --reload"
echo "   2. Install frontend dependencies: cd frontend && npm install"
echo "   3. Start the React frontend: cd frontend && npm start"
echo ""
echo "📚 Sample users created:"
echo "   - alice.johnson@university.edu (CS Graduate, ML enthusiast)"
echo "   - bob.smith@college.edu (Physics Undergraduate)"
echo "   - carol.williams@university.edu (Psychology PhD)"
echo "   - david.brown@institute.edu (Engineering Student)"
echo "   - emma.davis@college.edu (Business Student)"
echo ""
echo "🔐 Default password for all sample users: 'password123'"
echo "    (Remember to change this in production!)"
echo ""
echo "Happy learning! 🎓"