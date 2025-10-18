#!/bin/bash

# Intelligent Matchmaking System - Production Deployment Script
# This script sets up and deploys the complete system using Docker Compose

set -e  # Exit on any error

echo "🚀 Intelligent Matchmaking System - Production Deployment"
echo "======================================================"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker and Docker Compose are installed
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    print_success "Prerequisites check passed!"
}

# Create necessary directories
create_directories() {
    print_status "Creating necessary directories..."
    
    mkdir -p nginx/ssl
    mkdir -p monitoring/grafana/dashboards
    mkdir -p monitoring/grafana/provisioning
    mkdir -p logs
    
    print_success "Directories created!"
}

# Generate environment file if it doesn't exist
generate_env_file() {
    print_status "Setting up environment configuration..."
    
    if [ ! -f .env ]; then
        cat > .env << EOF
# Database Configuration
MONGODB_URL=mongodb://admin:matchmaking_admin_2024@mongodb:27017/intelligent_matchmaking?authSource=admin
DATABASE_NAME=intelligent_matchmaking
REDIS_URL=redis://:matchmaking_redis_2024@redis:6379

# Security Configuration
SECRET_KEY=your_super_secret_key_here_change_in_production_$(date +%s)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://localhost

# Email Configuration (Update these with your actual credentials)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
EMAIL_FROM=your_email@gmail.com

# Application Settings
APP_NAME=Intelligent Matchmaking System
DEBUG=false
LOG_LEVEL=INFO

# Frontend Configuration
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000/ws
REACT_APP_NAME=Intelligent Matchmaking System
EOF
        
        print_warning "Generated .env file with default values."
        print_warning "Please update the email credentials and secret key in .env file before production use!"
    else
        print_status ".env file already exists, skipping generation."
    fi
}

# Setup monitoring configuration
setup_monitoring() {
    print_status "Setting up monitoring configuration..."
    
    # Create Prometheus configuration
    mkdir -p monitoring
    cat > monitoring/prometheus.yml << EOF
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'backend'
    static_configs:
      - targets: ['backend:8000']
    scrape_interval: 30s
    metrics_path: /metrics
  
  - job_name: 'ml-service'
    static_configs:
      - targets: ['ml_service:8001']
    scrape_interval: 30s
    metrics_path: /metrics
  
  - job_name: 'nginx'
    static_configs:
      - targets: ['nginx:80']
    scrape_interval: 30s
EOF
    
    print_success "Monitoring configuration created!"
}

# Build and start services
deploy_services() {
    print_status "Building and starting services..."
    
    # Stop any existing containers
    docker-compose down --remove-orphans
    
    # Build images
    print_status "Building Docker images..."
    docker-compose build --no-cache
    
    # Start core services first
    print_status "Starting database services..."
    docker-compose up -d mongodb redis
    
    # Wait for databases to be ready
    print_status "Waiting for databases to be ready..."
    sleep 30
    
    # Start application services
    print_status "Starting application services..."
    docker-compose up -d backend ml_service
    
    # Wait for backend to be ready
    sleep 20
    
    # Start frontend and nginx
    print_status "Starting frontend and proxy services..."
    docker-compose up -d frontend nginx
    
    # Start monitoring (optional)
    print_status "Starting monitoring services..."
    docker-compose up -d prometheus grafana
    
    print_success "All services started successfully!"
}

# Initialize database with sample data
initialize_database() {
    print_status "Initializing database with sample data..."
    
    # Wait for backend to be fully ready
    sleep 30
    
    # Create realistic users
    print_status "Creating realistic users..."
    docker-compose exec backend python /app/database/create_realistic_users.py
    
    print_success "Database initialized with sample data!"
}

# Health check
health_check() {
    print_status "Performing health checks..."
    
    services=("mongodb:27017" "redis:6379" "backend:8000" "frontend:3000" "ml_service:8001")
    
    for service in "${services[@]}"; do
        service_name=${service%:*}
        port=${service#*:}
        
        if docker-compose exec $service_name nc -z localhost $port 2>/dev/null; then
            print_success "$service_name is healthy"
        else
            print_warning "$service_name might not be ready yet"
        fi
    done
}

# Display access information
display_access_info() {
    print_success "🎉 Deployment completed successfully!"
    echo ""
    echo "==============================================="
    echo "  SYSTEM ACCESS INFORMATION"
    echo "==============================================="
    echo ""
    echo "🌐 Frontend Application: http://localhost:3000"
    echo "🔌 Backend API: http://localhost:8000"
    echo "📚 API Documentation: http://localhost:8000/docs"
    echo "🤖 ML Service: http://localhost:8001"
    echo "📊 Grafana Dashboard: http://localhost:3001 (admin/matchmaking_grafana_2024)"
    echo "📈 Prometheus: http://localhost:9090"
    echo ""
    echo "==============================================="
    echo "  SAMPLE LOGIN CREDENTIALS"
    echo "==============================================="
    echo ""
    echo "👨‍🎓 Student Login:"
    echo "   Email: arjun.patel@student.edu"
    echo "   Password: student123"
    echo ""
    echo "👩‍🏫 Teacher Login:"
    echo "   Email: rajesh.khanna@university.edu"
    echo "   Password: teacher123"
    echo ""
    echo "==============================================="
    echo "  USEFUL COMMANDS"
    echo "==============================================="
    echo ""
    echo "📋 View logs: docker-compose logs -f [service_name]"
    echo "🔄 Restart service: docker-compose restart [service_name]"
    echo "⏹️  Stop all services: docker-compose down"
    echo "🗑️  Clean up: docker-compose down -v --remove-orphans"
    echo "📊 View running services: docker-compose ps"
    echo ""
}

# Cleanup function
cleanup() {
    if [ "$1" == "full" ]; then
        print_warning "Performing full cleanup..."
        docker-compose down -v --remove-orphans
        docker system prune -af
        print_success "Full cleanup completed!"
    else
        print_status "Stopping services..."
        docker-compose down
        print_success "Services stopped!"
    fi
}

# Main deployment function
main() {
    case "$1" in
        "deploy")
            check_prerequisites
            create_directories
            generate_env_file
            setup_monitoring
            deploy_services
            initialize_database
            health_check
            display_access_info
            ;;
        "start")
            docker-compose up -d
            print_success "Services started!"
            ;;
        "stop")
            docker-compose down
            print_success "Services stopped!"
            ;;
        "restart")
            docker-compose restart
            print_success "Services restarted!"
            ;;
        "logs")
            docker-compose logs -f ${2:-}
            ;;
        "status")
            docker-compose ps
            ;;
        "cleanup")
            cleanup $2
            ;;
        "health")
            health_check
            ;;
        *)
            echo "Intelligent Matchmaking System - Deployment Script"
            echo ""
            echo "Usage: $0 {deploy|start|stop|restart|logs|status|cleanup|health}"
            echo ""
            echo "Commands:"
            echo "  deploy   - Full deployment (first time setup)"
            echo "  start    - Start all services"
            echo "  stop     - Stop all services"  
            echo "  restart  - Restart all services"
            echo "  logs     - View logs (optionally specify service name)"
            echo "  status   - Show service status"
            echo "  cleanup  - Clean up containers (use 'full' for complete cleanup)"
            echo "  health   - Check service health"
            echo ""
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"