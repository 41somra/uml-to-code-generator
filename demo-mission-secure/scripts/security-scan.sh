#!/bin/bash
# Container Security Scanning Script for Kessel Run

set -euo pipefail

IMAGE_NAME="${1:-kessel-run-service:latest}"
REPORT_DIR="security-reports"

echo "🔒 Starting security scan for image: $IMAGE_NAME"

# Create reports directory
mkdir -p "$REPORT_DIR"

# Trivy vulnerability scanning
echo "📊 Running Trivy vulnerability scan..."
trivy image --format json --output "$REPORT_DIR/trivy-report.json" "$IMAGE_NAME"
trivy image --format table "$IMAGE_NAME"

# Container structure test
echo "🏗️ Running container structure tests..."
if command -v container-structure-test &> /dev/null; then
    container-structure-test test --image "$IMAGE_NAME" --config container-test.yaml
fi

# Docker Bench for Security (if running on Docker)
echo "🛡️ Running Docker Bench for Security..."
if command -v docker-bench-security &> /dev/null; then
    docker-bench-security --json --log-level WARN > "$REPORT_DIR/docker-bench-report.json"
fi

# Anchore scanning (if available)
echo "⚓ Running Anchore analysis..."
if command -v anchore-cli &> /dev/null; then
    anchore-cli image add "$IMAGE_NAME"
    anchore-cli image wait "$IMAGE_NAME"
    anchore-cli image vuln "$IMAGE_NAME" all > "$REPORT_DIR/anchore-vulns.json"
fi

echo "✅ Security scanning completed. Reports available in: $REPORT_DIR"

# Exit with error if critical vulnerabilities found
CRITICAL_COUNT=$(jq '.Results[]?.Vulnerabilities[]? | select(.Severity == "CRITICAL") | length' "$REPORT_DIR/trivy-report.json" | wc -l)
if [ "$CRITICAL_COUNT" -gt 0 ]; then
    echo "❌ Critical vulnerabilities found: $CRITICAL_COUNT"
    exit 1
fi

echo "🎉 No critical vulnerabilities found!"
