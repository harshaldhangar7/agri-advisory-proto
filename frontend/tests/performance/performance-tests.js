/**
 * Frontend Performance Testing Script
 * Measures: Load time, API response time, rendering performance
 * Usage: Run in browser console or with Node.js
 */

const FRONTEND_URL = 'http://localhost:5174';
const API_URL = 'http://localhost:8000/api';
const API_KEY = 'default-dev-key';

// ============================================================================
// PERFORMANCE MEASUREMENT UTILITIES
// ============================================================================

class PerformanceMonitor {
  constructor() {
    this.measurements = {};
    this.apiCalls = [];
  }

  /**
   * Measure page load time
   */
  async measurePageLoadTime() {
    const startTime = performance.now();
    
    // Wait for major components to load
    return new Promise(resolve => {
      window.addEventListener('load', () => {
        const endTime = performance.now();
        const loadTime = endTime - startTime;
        this.measurements['pageLoadTime'] = loadTime;
        console.log(`✓ Page Load Time: ${loadTime.toFixed(2)}ms`);
        resolve(loadTime);
      });
    });
  }

  /**
   * Measure First Contentful Paint (FCP)
   */
  measureFCP() {
    const paintEntries = performance.getEntriesByType('paint');
    const fcp = paintEntries.find(entry => entry.name === 'first-contentful-paint');
    
    if (fcp) {
      this.measurements['FCP'] = fcp.startTime;
      console.log(`✓ First Contentful Paint: ${fcp.startTime.toFixed(2)}ms`);
      return fcp.startTime;
    }
    return null;
  }

  /**
   * Measure Largest Contentful Paint (LCP)
   */
  observeLCP() {
    return new Promise(resolve => {
      const observer = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        const lastEntry = entries[entries.length - 1];
        this.measurements['LCP'] = lastEntry.startTime;
        console.log(`✓ Largest Contentful Paint: ${lastEntry.startTime.toFixed(2)}ms`);
      });
      
      observer.observe({ entryTypes: ['largest-contentful-paint'] });
      
      // Stop observing after 5 seconds
      setTimeout(() => {
        observer.disconnect();
        resolve();
      }, 5000);
    });
  }

  /**
   * Measure API call response time
   */
  async measureAPICall(method, endpoint, data = null) {
    const startTime = performance.now();
    
    try {
      const config = {
        method,
        headers: {
          'x-api-key': API_KEY,
          'Content-Type': 'application/json'
        }
      };
      
      if (data) {
        config.body = JSON.stringify(data);
      }
      
      const response = await fetch(`${API_URL}${endpoint}`, config);
      const endTime = performance.now();
      const duration = endTime - startTime;
      
      this.apiCalls.push({
        method,
        endpoint,
        duration,
        status: response.status,
        timestamp: new Date().toISOString()
      });
      
      console.log(`✓ API ${method} ${endpoint}: ${duration.toFixed(2)}ms (Status: ${response.status})`);
      return { duration, status: response.status, data: await response.json() };
    } catch (error) {
      const endTime = performance.now();
      const duration = endTime - startTime;
      console.error(`✗ API Error: ${error.message} (${duration.toFixed(2)}ms)`);
      return { duration, error: error.message };
    }
  }

  /**
   * Measure Cumulative Layout Shift (CLS)
   */
  observeCLS() {
    let clsValue = 0;
    
    const observer = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        if (!entry.hadRecentInput) {
          clsValue += entry.value;
        }
      }
    });
    
    observer.observe({ entryTypes: ['layout-shift'] });
    
    this.measurements['CLS'] = clsValue;
    return { observer, getValue: () => clsValue };
  }

  /**
   * Get memory usage (if available)
   */
  getMemoryUsage() {
    if (performance.memory) {
      const memory = {
        usedJSHeapSize: (performance.memory.usedJSHeapSize / 1048576).toFixed(2),
        totalJSHeapSize: (performance.memory.totalJSHeapSize / 1048576).toFixed(2),
        jsHeapSizeLimit: (performance.memory.jsHeapSizeLimit / 1048576).toFixed(2)
      };
      console.log(`✓ Memory Usage: ${memory.usedJSHeapSize}MB / ${memory.totalJSHeapSize}MB (Limit: ${memory.jsHeapSizeLimit}MB)`);
      return memory;
    }
    return null;
  }

  /**
   * Generate report
   */
  generateReport() {
    console.log('\n' + '='.repeat(80));
    console.log('PERFORMANCE TEST REPORT');
    console.log('='.repeat(80));
    
    console.log('\n📊 PAGE METRICS:');
    for (const [key, value] of Object.entries(this.measurements)) {
      if (typeof value === 'number') {
        console.log(`  ${key}: ${value.toFixed(2)}ms`);
      }
    }
    
    console.log('\n🔗 API CALL PERFORMANCE:');
    if (this.apiCalls.length > 0) {
      const avgDuration = this.apiCalls.reduce((sum, call) => sum + call.duration, 0) / this.apiCalls.length;
      console.log(`  Total Calls: ${this.apiCalls.length}`);
      console.log(`  Average Response Time: ${avgDuration.toFixed(2)}ms`);
      console.log(`  Min Response Time: ${Math.min(...this.apiCalls.map(c => c.duration)).toFixed(2)}ms`);
      console.log(`  Max Response Time: ${Math.max(...this.apiCalls.map(c => c.duration)).toFixed(2)}ms`);
      console.log('\n  Individual Calls:');
      this.apiCalls.forEach(call => {
        console.log(`    ${call.method} ${call.endpoint}: ${call.duration.toFixed(2)}ms`);
      });
    }
    
    console.log('\n💾 MEMORY:');
    const memory = this.getMemoryUsage();
    if (!memory) {
      console.log('  (Not available in this browser)');
    }
    
    console.log('\n✅ RECOMMENDATIONS:');
    const recommendations = this.getRecommendations();
    recommendations.forEach(rec => console.log(`  - ${rec}`));
    
    console.log('\n' + '='.repeat(80));
  }

  /**
   * Generate recommendations based on metrics
   */
  getRecommendations() {
    const recommendations = [];
    
    if (this.measurements['pageLoadTime'] > 3000) {
      recommendations.push('Page load time > 3s: Consider code splitting, lazy loading, or CDN');
    }
    
    if (this.measurements['FCP'] > 1500) {
      recommendations.push('FCP > 1.5s: Optimize critical rendering path');
    }
    
    if (this.measurements['LCP'] > 2500) {
      recommendations.push('LCP > 2.5s: Optimize large images or heavy DOM operations');
    }
    
    if (this.measurements['CLS'] > 0.1) {
      recommendations.push('CLS > 0.1: Fix layout shifts in forms and messages');
    }
    
    const avgApiTime = this.apiCalls.reduce((sum, call) => sum + call.duration, 0) / this.apiCalls.length;
    if (avgApiTime > 1000) {
      recommendations.push('Average API response > 1s: Optimize backend or reduce payload size');
    }
    
    const memory = performance.memory;
    if (memory && memory.usedJSHeapSize > 50000000) { // 50MB
      recommendations.push('Memory usage > 50MB: Check for memory leaks');
    }
    
    if (recommendations.length === 0) {
      recommendations.push('All metrics within acceptable ranges!');
    }
    
    return recommendations;
  }
}

// ============================================================================
// TEST SCENARIOS
// ============================================================================

async function runPerformanceTests() {
  const monitor = new PerformanceMonitor();

  console.log('🚀 Starting Performance Tests...\n');
  
  // 1. Measure page load
  console.log('📄 Test 1: Page Load Time');
  monitor.measureFCP();
  await monitor.observeLCP();
  
  // 2. Measure API calls
  console.log('\n🔗 Test 2: API Call Performance');
  
  // Test 2a: Create farmer
  await monitor.measureAPICall('POST', '/farmers/', {
    name: 'Performance Test Farmer',
    phone: '9876543210',
    language: 'mr'
  });
  
  // Test 2b: List farmers
  await monitor.measureAPICall('GET', '/farmers/');
  
  // Test 2c: Create plot (if farmer exists)
  const farmerResult = await monitor.measureAPICall('POST', '/farmers/', {
    name: 'Plot Test Farmer',
    phone: null,
    language: 'mr'
  });
  
  if (farmerResult.data && farmerResult.data.id) {
    const farmerId = farmerResult.data.id;
    
    await monitor.measureAPICall('POST', `/farmers/${farmerId}/plots`, {
      name: 'Test Plot',
      crop: 'Wheat',
      area_hectares: 5
    });
    
    // Test 2d: Get advisory
    const plotResult = await monitor.measureAPICall('GET', `/farmers/${farmerId}`);
    if (plotResult.data && plotResult.data.plots && plotResult.data.plots.length > 0) {
      const plotId = plotResult.data.plots[0].id;
      
      await monitor.measureAPICall('POST', '/advisory/recommend', {
        plot_id: plotId,
        symptoms: 'Yellow leaves',
        weather: { rain_last_3_days: 0 }
      });
    }
  }
  
  // 3. Measure CLS
  console.log('\n🎨 Test 3: Layout Stability');
  const cls = monitor.observeCLS();
  
  // 4. Measure memory
  console.log('\n💾 Test 4: Memory Usage');
  monitor.getMemoryUsage();
  
  // 5. Generate report
  setTimeout(() => {
    monitor.generateReport();
  }, 5000);
  
  return monitor;
}

// ============================================================================
// RUN TESTS
// ============================================================================

// To run: Copy and paste in browser console
console.log('Performance testing available. Run: runPerformanceTests()');

// Or for automated testing:
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    PerformanceMonitor,
    runPerformanceTests
  };
}
