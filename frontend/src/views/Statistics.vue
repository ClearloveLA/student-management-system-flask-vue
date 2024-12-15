<template>
  <div class="container-fluid mt-4">
    <!-- 顶部统计卡片 -->
    <div class="row g-4 mb-4">
      <div class="col-xl-3 col-md-6">
        <div class="stat-card bg-primary text-white">
          <div class="stat-card-body">
            <div class="d-flex align-items-center">
              <div class="stat-icon">
                <i class="bi bi-people-fill"></i>
              </div>
              <div class="ms-3">
                <h6 class="mb-1">总学生数</h6>
                <h3 class="mb-0">{{ stats.total_students || 0 }}</h3>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-xl-3 col-md-6">
        <div class="stat-card bg-success text-white">
          <div class="stat-card-body">
            <div class="d-flex align-items-center">
              <div class="stat-icon">
                <i class="bi bi-gender-ambiguous"></i>
              </div>
              <div class="ms-3">
                <h6 class="mb-1">男女比例</h6>
                <h3 class="mb-0">
                  {{ calculateGenderRatio() }}
                </h3>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-xl-3 col-md-6">
        <div class="stat-card bg-info text-white">
          <div class="stat-card-body">
            <div class="d-flex align-items-center">
              <div class="stat-icon">
                <i class="bi bi-mortarboard-fill"></i>
              </div>
              <div class="ms-3">
                <h6 class="mb-1">专业数量</h6>
                <h3 class="mb-0">
                  {{ Object.keys(stats.major_distribution || {}).length }}
                </h3>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-xl-3 col-md-6">
        <div class="stat-card bg-warning text-white">
          <div class="stat-card-body">
            <div class="d-flex align-items-center">
              <div class="stat-icon">
                <i class="bi bi-building"></i>
              </div>
              <div class="ms-3">
                <h6 class="mb-1">班级数量</h6>
                <h3 class="mb-0">
                  {{ Object.keys(stats.class_distribution || {}).length }}
                </h3>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 图表区域 -->
    <div class="row g-4">
      <div class="col-xl-4">
        <div class="chart-card">
          <div class="chart-card-header">
            <h5>性别分布</h5>
          </div>
          <div class="chart-card-body">
            <div class="chart-container">
              <canvas ref="genderChart"></canvas>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-xl-8">
        <div class="chart-card">
          <div class="chart-card-header">
            <h5>专业分布</h5>
          </div>
          <div class="chart-card-body">
            <div class="chart-container">
              <canvas ref="majorChart"></canvas>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-xl-8">
        <div class="chart-card">
          <div class="chart-card-header">
            <h5>班级分布</h5>
          </div>
          <div class="chart-card-body">
            <div class="chart-container">
              <canvas ref="classChart"></canvas>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-xl-4">
        <div class="chart-card">
          <div class="chart-card-header">
            <h5>年龄分布</h5>
          </div>
          <div class="chart-card-body">
            <div class="chart-container">
              <canvas ref="ageChart"></canvas>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getStudentStats } from '@/api/student'
import { ElMessage } from 'element-plus'
import Chart from 'chart.js/auto'

const stats = ref({})
const genderChart = ref(null)
const majorChart = ref(null)
const classChart = ref(null)
const ageChart = ref(null)

let charts = {}

// 计算男女比例
const calculateGenderRatio = () => {
  const distribution = stats.value.gender_distribution || {}
  const male = distribution['男'] || 0
  const female = distribution['女'] || 0
  return `${male}:${female}`
}

// 加载统计数据
const loadStats = async () => {
  try {
    const data = await getStudentStats()
    stats.value = data
    renderCharts()
  } catch (error) {
    console.error('加载统计数据失败:', error)
    ElMessage.error('加载统计数据失败')
  }
}

// 渲染图表
const renderCharts = () => {
  // 清除旧图表
  Object.values(charts).forEach(chart => chart?.destroy())
  
  // 性别分布环形图
  charts.gender = new Chart(genderChart.value, {
    type: 'doughnut',
    data: {
      labels: Object.keys(stats.value.gender_distribution || {}),
      datasets: [{
        data: Object.values(stats.value.gender_distribution || {}),
        backgroundColor: ['#36A2EB', '#FF6384'],
        borderWidth: 2,
        borderColor: '#fff'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom'
        }
      },
      cutout: '60%'
    }
  })
  
  // 专业分布柱状图
  charts.major = new Chart(majorChart.value, {
    type: 'bar',
    data: {
      labels: Object.keys(stats.value.major_distribution || {}),
      datasets: [{
        label: '学生数量',
        data: Object.values(stats.value.major_distribution || {}),
        backgroundColor: '#4BC0C0',
        borderRadius: 6,
        borderWidth: 0
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          grid: {
            drawBorder: false
          }
        },
        x: {
          grid: {
            display: false
          }
        }
      }
    }
  })
  
  // 班级分布柱状图
  charts.class = new Chart(classChart.value, {
    type: 'bar',
    data: {
      labels: Object.keys(stats.value.class_distribution || {}),
      datasets: [{
        label: '学生数量',
        data: Object.values(stats.value.class_distribution || {}),
        backgroundColor: '#FFCE56',
        borderRadius: 6,
        borderWidth: 0
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          grid: {
            drawBorder: false
          }
        },
        x: {
          grid: {
            display: false
          }
        }
      }
    }
  })
  
  // 年龄分布面积图
  charts.age = new Chart(ageChart.value, {
    type: 'line',
    data: {
      labels: Object.keys(stats.value.age_distribution || {}),
      datasets: [{
        label: '学生数量',
        data: Object.values(stats.value.age_distribution || {}),
        borderColor: '#FF9F40',
        backgroundColor: 'rgba(255, 159, 64, 0.2)',
        fill: true,
        tension: 0.4,
        pointRadius: 4,
        pointHoverRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          grid: {
            drawBorder: false
          }
        },
        x: {
          grid: {
            display: false
          }
        }
      }
    }
  })
}

onMounted(() => {
  loadStats()
})
</script>

<style scoped>
.stat-card {
  padding: 1.5rem;
  border-radius: 1rem;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
  transition: transform 0.3s;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
}

.stat-icon i {
  font-size: 1.5rem;
}

.chart-card {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.08);
  overflow: hidden;
  height: 100%;
}

.chart-card-header {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  background: #f8f9fa;
}

.chart-card-header h5 {
  margin: 0;
  color: #495057;
  font-weight: 600;
}

.chart-card-body {
  padding: 1.5rem;
}

.chart-container {
  position: relative;
  height: 300px;
  width: 100%;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .chart-container {
    height: 250px;
  }
}
</style> 