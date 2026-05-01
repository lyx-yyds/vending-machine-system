<template>
  <div class="vending-login">
    <div class="login-left">
      <div class="brand-section">
        <div class="logo-icon">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="3" y="3" width="18" height="18" rx="3" stroke="currentColor" stroke-width="2"/>
            <path d="M3 9H21" stroke="currentColor" stroke-width="2"/>
            <path d="M9 21V9" stroke="currentColor" stroke-width="2"/>
            <circle cx="6" cy="15" r="1.5" fill="currentColor"/>
            <circle cx="6" cy="12" r="1.5" fill="currentColor"/>
            <circle cx="15" cy="15" r="1.5" fill="currentColor"/>
            <circle cx="15" cy="12" r="1.5" fill="currentColor"/>
            <circle cx="15" cy="6" r="1.5" fill="currentColor"/>
          </svg>
        </div>
        <h1>智能售货系统</h1>
        <p>Smart Vending Machine</p>
      </div>

      <div class="products-showcase">
        <div class="section-title">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M6 2L3 6V20C3 20.5304 3.21071 21.0391 3.58579 21.4142C3.96086 21.7893 4.46957 22 5 22H19C19.5304 22 20.0391 21.7893 20.4142 21.4142C20.7893 21.0391 21 20.5304 21 20V6L18 2H6Z" stroke="currentColor" stroke-width="2"/>
            <path d="M3 6H21" stroke="currentColor" stroke-width="2"/>
            <path d="M16 10C16 11.0609 15.5786 12.0783 14.8284 12.8284C14.0783 13.5786 13.0609 14 12 14C10.9391 14 9.92172 13.5786 9.17157 12.8284C8.42143 12.0783 8 11.0609 8 10" stroke="currentColor" stroke-width="2"/>
          </svg>
          <span>热门商品</span>
        </div>

        <div class="products-grid">
          <div v-for="(product, index) in products" :key="index" class="product-card">
            <div class="product-icon" :style="{ backgroundColor: product.color + '20', borderColor: product.color }">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M9 2C7.89543 2 7 2.89543 7 4C7 5.10457 7.89543 6 9 6C10.1046 6 11 5.10457 11 4C11 2.89543 10.1046 2 9 2Z" :fill="product.color"/>
                <path d="M15 2C13.8954 2 13 2.89543 13 4C13 5.10457 13.8954 6 15 6C16.1046 6 17 5.10457 17 4C17 2.89543 16.1046 2 15 2Z" :fill="product.color"/>
                <path d="M7 8H17L19 22H5L7 8Z" :stroke="product.color" stroke-width="2"/>
              </svg>
            </div>
            <span class="product-name">{{ product.name }}</span>
            <span class="product-price">{{ product.price }}</span>
          </div>
        </div>
      </div>

      <div class="features-bar">
        <div class="feature-item">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M20.84 4.61C20.3292 4.09904 19.7228 3.69364 19.0554 3.41708C18.3879 3.14052 17.6725 2.99817 16.95 2.99817C16.2275 2.99817 15.5121 3.14052 14.8446 3.41708C14.1772 3.69364 13.5708 4.09904 13.06 4.61L12 5.67L10.94 4.61C9.9083 3.57831 8.50903 2.99871 7.05 2.99871C5.59096 2.99871 4.19169 3.57831 3.16 4.61C2.1283 5.6417 1.54871 7.04097 1.54871 8.5C1.54871 9.95903 2.1283 11.3583 3.16 12.39L4.22 13.45L12 21.23L19.78 13.45L20.84 12.39C21.351 11.8792 21.7564 11.2728 22.0329 10.6054C22.3095 9.93791 22.4518 9.22249 22.4518 8.5C22.4518 7.77751 22.3095 7.0621 22.0329 6.39464C21.7564 5.72718 21.351 5.12075 20.84 4.61Z" stroke="currentColor" stroke-width="2"/>
          </svg>
          <span>品质保障</span>
        </div>
        <div class="feature-item">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 22C12 22 20 18 20 12V5L12 2L4 5V12C4 18 12 22 12 22Z" stroke="currentColor" stroke-width="2"/>
          </svg>
          <span>快速配送</span>
        </div>
        <div class="feature-item">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z" stroke="currentColor" stroke-width="2"/>
          </svg>
          <span>优质服务</span>
        </div>
      </div>
    </div>

    <div class="login-right">
      <div class="login-card">
        <div class="card-header">
          <h2>欢迎回来</h2>
          <p>请登录您的账户继续购物</p>
        </div>

        <form class="login-form" @submit.prevent="handleLogin">
          <div class="form-item">
            <label>用户名</label>
            <div class="input-wrapper">
              <svg class="input-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M20 21V19C20 17.9391 19.5786 16.9217 18.8284 16.1716C18.0783 15.4214 17.0609 15 16 15H8C6.93913 15 5.92172 15.4214 5.17157 16.1716C4.42143 16.9217 4 17.9391 4 19V21" stroke="currentColor" stroke-width="2"/>
                <path d="M12 11C14.2091 11 16 9.20914 16 7C16 4.79086 14.2091 3 12 3C9.79086 3 8 4.79086 8 7C8 9.20914 9.79086 11 12 11Z" stroke="currentColor" stroke-width="2"/>
              </svg>
              <input
                v-model="loginForm.username"
                type="text"
                placeholder="请输入用户名"
                :disabled="loading"
              />
            </div>
          </div>

          <div class="form-item">
            <label>密码</label>
            <div class="input-wrapper password-input">
              <svg class="input-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2" stroke="currentColor" stroke-width="2"/>
                <path d="M7 11V7C7 5.93913 7.42143 4.92172 8.17157 4.17157C8.92172 3.42143 9.93913 3 11 3H13C14.0609 3 15.0783 3.42143 15.8284 4.17157C16.5786 4.92172 17 5.93913 17 7V11" stroke="currentColor" stroke-width="2"/>
              </svg>
              <input
                v-model="loginForm.password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="请输入密码"
                :disabled="loading"
              />
              <button type="button" class="toggle-password" @click="showPassword = !showPassword">
                <svg v-if="showPassword" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M1 12C1 12 5 4 12 4C19 4 23 12 23 12C23 12 19 20 12 20C5 20 1 12 1 12Z" stroke="currentColor" stroke-width="2"/>
                  <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/>
                </svg>
                <svg v-else viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M1 12C1 12 5 4 12 4C19 4 23 12 23 12C23 12 19 20 12 20C5 20 1 12 1 12Z" stroke="currentColor" stroke-width="2"/>
                  <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/>
                  <path d="M3 3L21 21" stroke="currentColor" stroke-width="2"/>
                </svg>
              </button>
            </div>
          </div>

          <div class="form-options">
            <label class="remember">
              <input type="checkbox" v-model="loginForm.remember" />
              <span>记住我</span>
            </label>
            <a href="#" class="forgot">忘记密码？</a>
          </div>

          <div v-if="errorMsg" class="error-message">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
              <path d="M12 8V12" stroke="currentColor" stroke-width="2"/>
              <circle cx="12" cy="16" r="1" fill="currentColor"/>
            </svg>
            {{ errorMsg }}
          </div>

          <button type="submit" class="login-btn" :disabled="loading">
            <span v-if="loading" class="loading-spinner"></span>
            <span v-else>
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M15 3H19C19.5304 3 20.0391 3.21071 20.4142 3.58579C20.7893 3.96086 21 4.46957 21 5V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H15" stroke="currentColor" stroke-width="2"/>
                <path d="M10 17L15 12L10 7" stroke="currentColor" stroke-width="2"/>
                <path d="M15 12H3" stroke="currentColor" stroke-width="2"/>
              </svg>
              登 录
            </span>
          </button>

          <div class="divider">
            <span>或</span>
          </div>

          <button type="button" class="register-btn">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M16 21V19C16 17.9391 15.5786 16.9217 14.8284 16.1716C14.0783 15.4214 13.0609 15 12 15C10.9391 15 9.92172 15.4214 9.17157 16.1716C8.42143 16.9217 8 17.9391 8 19V21" stroke="currentColor" stroke-width="2"/>
              <path d="M12 11C14.2091 11 16 9.20914 16 7C16 4.79086 14.2091 3 12 3C9.79086 3 8 4.79086 8 7C8 9.20914 9.79086 11 12 11Z" stroke="currentColor" stroke-width="2"/>
              <path d="M20 8V14" stroke="currentColor" stroke-width="2"/>
              <path d="M17 11H23" stroke="currentColor" stroke-width="2"/>
            </svg>
            注册新账户
          </button>
        </form>

        <!-- <div class="social-login">
          <p>其他登录方式</p>
          <div class="social-icons">
            <button class="social-btn wechat">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M8.691 2C5.927 2 3.667 3.241 3.667 3.241L2 9.5C2 9.5 4.24 10.5 6.5 10.5C6.5 10.5 4.333 11 3.667 13C3.667 13 4.666 12 6.5 12C8.334 12 9.333 13 9.333 13L8.691 2Z" fill="currentColor"/>
                <path d="M9.333 21C9.333 21 14 19 14 13.5C14 13.5 11.5 14.5 9.333 14.5C7.166 14.5 4.666 13.5 4.666 13.5L3.667 18C3.667 18 5.999 19.5 9.333 21Z" fill="currentColor"/>
                <path d="M18.666 11C16.732 11 15.166 10.5 15.166 10.5C15.166 10.5 17.4 9.5 19.666 9.5L21.333 3.241C21.333 3.241 19.073 2 16.309 2C13.545 2 11.285 3.241 11.285 3.241L9.333 18.5C9.333 18.5 11.593 21 16.309 21C20.027 21 21.999 19.5 21.999 19.5L18.666 11Z" fill="currentColor"/>
                <path d="M17 6C17.552 6 18 5.552 18 5C18 4.448 17.552 4 17 4C16.448 4 16 4.448 16 5C16 5.552 16.448 6 17 6Z" fill="white"/>
                <path d="M21 6C21.552 6 22 5.552 22 5C22 4.448 21.552 4 21 4C20.448 4 20 4.448 20 5C20 5.552 20.448 6 21 6Z" fill="white"/>
              </svg>
            </button>
            <button class="social-btn qq">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2L14.5 8H21L15.5 12L17.5 19L12 15L6.5 19L8.5 12L3 8H9.5L12 2Z" fill="currentColor"/>
              </svg>
            </button>
            <button class="social-btn weibo">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
                <path d="M8 14C8.5 15.5 10 17 12 17C14 17 15.5 15.5 16 14" stroke="currentColor" stroke-width="2"/>
                <path d="M16 8C17.5 8.5 18 10 17 11C16 12 14 12 13 11C12.5 10.5 13 9 14 9" stroke="currentColor" stroke-width="2"/>
              </svg>
            </button>
          </div>
        </div> -->
      </div>

      <div class="login-footer">
        <p>登录即表示同意 <a href="#">服务条款</a> 和 <a href="#">隐私政策</a></p>
      </div>
    </div>

    <div class="decoration">
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
      <div class="circle circle-3"></div>
    </div>
  </div>
</template>

<style scoped>
.vending-login {
  min-height: 100vh;
  display: flex;
  background: linear-gradient(135deg, #FF6B35 0%, #F7931E 50%, #FFD23F 100%);
  position: relative;
  overflow: hidden;
}

.decoration {
  position: absolute;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.circle {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
}

.circle-1 {
  width: 400px;
  height: 400px;
  top: -100px;
  right: -100px;
  animation: float 8s ease-in-out infinite;
}

.circle-2 {
  width: 300px;
  height: 300px;
  bottom: -50px;
  left: -50px;
  animation: float 6s ease-in-out infinite reverse;
}

.circle-3 {
  width: 200px;
  height: 200px;
  top: 50%;
  left: 50%;
  animation: float 10s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0) scale(1); }
  50% { transform: translateY(-30px) scale(1.05); }
}

.login-left {
  flex: 1;
  padding: 60px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  color: white;
  position: relative;
  z-index: 1;
  max-width: 55%;
}

.brand-section {
  margin-bottom: 50px;
}

.logo-icon {
  width: 80px;
  height: 80px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.logo-icon svg {
  width: 50px;
  height: 50px;
}

.brand-section h1 {
  font-size: 42px;
  font-weight: 700;
  margin-bottom: 10px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

.brand-section p {
  font-size: 18px;
  opacity: 0.9;
  letter-spacing: 2px;
}

.products-showcase {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  padding: 30px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  margin-bottom: 40px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
  font-size: 18px;
  font-weight: 600;
}

.section-title svg {
  width: 24px;
  height: 24px;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
}

.product-card {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 16px;
  padding: 20px 15px;
  text-align: center;
  transition: all 0.3s ease;
  cursor: pointer;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.product-icon {
  width: 60px;
  height: 60px;
  margin: 0 auto 12px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid;
}

.product-icon svg {
  width: 35px;
  height: 35px;
}

.product-name {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: #333;
  margin-bottom: 5px;
}

.product-price {
  display: block;
  font-size: 16px;
  font-weight: 700;
  color: #FF6B35;
}

.features-bar {
  display: flex;
  gap: 40px;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  font-weight: 500;
}

.feature-item svg {
  width: 24px;
  height: 24px;
}

.login-right {
  width: 480px;
  height: 90vh;
  padding: 40px 60px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  background: white;
  position: relative;
  z-index: 1;
  margin: auto 0;
  border-radius: 30px 30px 30px 30px;
}

.login-card {
  background: white;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.card-header {
  text-align: center;
  margin-bottom: 35px;
}

.card-header h2 {
  font-size: 32px;
  font-weight: 700;
  color: #1a1a2e;
  margin-bottom: 10px;
}

.card-header p {
  color: #666;
  font-size: 14px;
}

.login-form {
  margin-bottom: 25px;
}

.form-item {
  margin-bottom: 20px;
}

.form-item label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 15px;
  width: 20px;
  height: 20px;
  color: #999;
  pointer-events: none;
}

.input-wrapper input {
  width: 100%;
  padding: 14px 14px 14px 48px;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  font-size: 14px;
  transition: all 0.3s ease;
  background: #fafafa;
}

.password-input input {
  padding-right: 48px;
}

.toggle-password {
  position: absolute;
  right: 12px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
  transition: color 0.3s;
}

.toggle-password:hover {
  color: #FF6B35;
}

.toggle-password svg {
  width: 20px;
  height: 20px;
}

.input-wrapper input:focus {
  outline: none;
  border-color: #FF6B35;
  background: white;
  box-shadow: 0 0 0 4px rgba(255, 107, 53, 0.1);
}

.input-wrapper input::placeholder {
  color: #aaa;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  font-size: 13px;
}

.remember {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  color: #666;
}

.remember input[type="checkbox"] {
  width: 16px;
  height: 16px;
  accent-color: #FF6B35;
  cursor: pointer;
}

.forgot {
  color: #FF6B35;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s;
}

.forgot:hover {
  color: #F7931E;
}

.error-message {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #FFF5F5;
  color: #E53E3E;
  padding: 12px 15px;
  border-radius: 10px;
  font-size: 13px;
  margin-bottom: 15px;
  border-left: 4px solid #E53E3E;
}

.error-message svg {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

.login-btn {
  width: 100%;
  padding: 16px;
  background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 6px 20px rgba(255, 107, 53, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.login-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(255, 107, 53, 0.5);
}

.login-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.login-btn svg {
  width: 20px;
  height: 20px;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.divider {
  display: flex;
  align-items: center;
  margin: 25px 0;
  color: #999;
  font-size: 13px;
}

.divider::before,
.divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: #e0e0e0;
}

.divider span {
  padding: 0 15px;
}

.register-btn {
  width: 100%;
  padding: 14px;
  background: white;
  color: #FF6B35;
  border: 2px solid #FF6B35;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.register-btn:hover {
  background: #FFF5F2;
  transform: translateY(-2px);
}

.register-btn svg {
  width: 18px;
  height: 18px;
}

.social-login {
  text-align: center;
  padding-top: 25px;
  border-top: 1px solid #eee;
}

.social-login p {
  font-size: 13px;
  color: #999;
  margin-bottom: 15px;
}

.social-icons {
  display: flex;
  justify-content: center;
  gap: 15px;
}

.social-btn {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  border: 2px solid #eee;
  background: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.social-btn svg {
  width: 24px;
  height: 24px;
}

.social-btn.wechat {
  color: #07C160;
}

.social-btn.wechat:hover {
  background: #07C160;
  color: white;
  border-color: #07C160;
}

.social-btn.qq {
  color: #12B7F5;
}

.social-btn.qq:hover {
  background: #12B7F5;
  color: white;
  border-color: #12B7F5;
}

.social-btn.weibo {
  color: #E6162D;
}

.social-btn.weibo:hover {
  background: #E6162D;
  color: white;
  border-color: #E6162D;
}

.login-footer {
  text-align: center;
  padding-top: 20px;
}

.login-footer p {
  font-size: 12px;
  color: #999;
}

.login-footer a {
  color: #FF6B35;
  text-decoration: none;
}

.login-footer a:hover {
  text-decoration: underline;
}

@media (max-width: 1200px) {
  .login-left {
    padding: 40px;
  }

  .brand-section h1 {
    font-size: 32px;
  }

  .products-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .login-right {
    width: 420px;
    padding: 40px;
  }
}

@media (max-width: 900px) {
  .vending-login {
    flex-direction: column;
  }

  .login-left {
    padding: 30px;
    flex: none;
  }

  .brand-section {
    margin-bottom: 30px;
    text-align: center;
  }

  .logo-icon {
    margin: 0 auto 15px;
  }

  .products-showcase {
    display: none;
  }

  .features-bar {
    justify-content: center;
  }

  .login-right {
    width: 100%;
    border-radius: 30px 30px 0 0;
    margin-top: 20px;
    padding: 30px;
  }
}
</style>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { login } from '@/api/user'

const router = useRouter()

const loginForm = ref({
  username: '',
  password: '',
  remember: false
})

const loading = ref(false)
const errorMsg = ref('')
const showPassword = ref(false)

const handleLogin = async () => {
  if (!loginForm.value.username || !loginForm.value.password) {
    errorMsg.value = '请输入用户名和密码'
    return
  }

  loading.value = true
  //const res = await login(loginForm)
  // console.log(res.data)
  // if (res.data.code === 2000) {
  //     ElMessage.success(res.data.message)
  //     sessionStorage.setItem('token', res.data.data.token)
  //     sessionStorage.setItem('user', JSON.stringify(res.data.data.user))
  //     sessionStorage.setItem('role_type', res.data.data.user.role_type)
  //     router.push('/backend')
  //   }

  try {
    const res = await login(loginForm.value)
    console.log('登录响应:', res)
    if (res.data.code === 2000) {
        ElMessage.success(res.data.message)
        sessionStorage.setItem('token', res.data.data.token)
        sessionStorage.setItem('user', JSON.stringify(res.data.data.user))
        sessionStorage.setItem('role_type', res.data.data.user.role_type)
        sessionStorage.setItem('user_id', res.data.data.user.id)
        router.push('/backend')
    } else {
        ElMessage.error(res.data.message || '登录失败')
    }
    } catch (error: any) {
        console.log('登录错误:', error)
        ElMessage.error(error.response?.data?.message || '登录失败，请检查网络或账号密码')
    } finally {
        loading.value = false
    }

}

const products = [
  { name: '可口可乐', price: '¥3.00', color: '#E61A27' },
  { name: '雪碧', price: '¥3.00', color: '#80C31C' },
  { name: '农夫山泉', price: '¥2.00', color: '#3B82F6' },
  { name: '芬达', price: '¥3.00', color: '#F97316' },
  { name: '奶茶', price: '¥8.00', color: '#92400E' },
  { name: '咖啡', price: '¥12.00', color: '#78350F' }
]
</script>

