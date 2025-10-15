class FaceDetectionApp {
    constructor() {
        this.video = document.getElementById('video');
        this.canvas = document.getElementById('canvas');
        this.capturedImg = document.getElementById('capturedImg');
        this.startCameraBtn = document.getElementById('startCamera');
        this.verifyBtn = document.getElementById('verifyBtn');
        this.resultSection = document.getElementById('resultSection');
        this.loading = document.getElementById('loading');
        this.results = document.getElementById('results');
        this.faceResults = document.getElementById('faceResults');
        this.status = document.getElementById('status');

        this.stream = null;
        this.capturedImageData = null;

        this.initEventListeners();
    }

    initEventListeners() {
        this.startCameraBtn.addEventListener('click', () => this.startCamera());
        this.verifyBtn.addEventListener('click', () => this.captureAndVerify());
    }

    async startCamera() {
        try {
            this.showStatus('Đang khởi động camera...', 'info');

            // Yêu cầu quyền truy cập camera
            this.stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    width: { ideal: 640 },
                    height: { ideal: 480 },
                    facingMode: 'user'
                }
            });

            this.video.srcObject = this.stream;

            // Đợi video load
            this.video.addEventListener('loadedmetadata', () => {
                this.showStatus('Camera đã sẵn sàng! Hãy đặt mặt vào khung và nhấn Verify', 'success');
                this.startCameraBtn.disabled = true;
                this.verifyBtn.disabled = false;
            });

        } catch (error) {
            console.error('Lỗi khi khởi động camera:', error);
            this.showStatus('Không thể truy cập camera. Vui lòng cho phép quyền truy cập camera.', 'error');
        }
    }

    captureAndVerify() {
        if (!this.stream) {
            this.showStatus('Vui lòng khởi động camera trước!', 'error');
            return;
        }

        try {
            // Capture ảnh từ video
            const context = this.canvas.getContext('2d');
            this.canvas.width = this.video.videoWidth;
            this.canvas.height = this.video.videoHeight;
            context.drawImage(this.video, 0, 0);

            // Lưu ảnh đã capture
            this.capturedImageData = this.canvas.toDataURL('image/jpeg', 0.8);
            this.capturedImg.src = this.capturedImageData;

            // Hiển thị section kết quả
            this.resultSection.style.display = 'block';
            this.loading.style.display = 'block';
            this.results.style.display = 'none';

            // Keep verify button enabled for continuous use

            // Gọi API
            this.analyzeImage();

        } catch (error) {
            console.error('Lỗi khi capture ảnh:', error);
            this.showStatus('Lỗi khi chụp ảnh!', 'error');
        }
    }

    async analyzeImage() {
        try {
            this.showStatus('Đang gửi ảnh để phân tích...', 'info');

            // Gửi request đến API
            const response = await fetch('http://localhost:5000/verify', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    image: this.capturedImageData,
                    employee_id: '2'
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            // Ẩn loading
            this.loading.style.display = 'none';

            // Hiển thị kết quả
            this.displayResults(data);

            // Re-enable verify button for next capture
            this.verifyBtn.disabled = false;

        } catch (error) {
            console.error('Lỗi khi gọi API:', error);
            this.loading.style.display = 'none';
            this.showStatus(`Lỗi khi phân tích: ${error.message}`, 'error');

            // Re-enable verify button even if there's an error
            this.verifyBtn.disabled = false;
        }
    }

    displayResults(data) {
        this.results.style.display = 'block';
        this.faceResults.innerHTML = '';

        if (data.error) {
            this.showStatus(`Lỗi từ API: ${data.error}`, 'error');
            return;
        }
        const faceDiv = document.createElement('div');
        faceDiv.innerHTML = `
                <div class="result-item">
                    <span class="result-label">Vị trí:</span>
                    <span class="result-value">x:${data.result.verify}</span>
                </div>
            `;

        this.faceResults.appendChild(faceDiv);
    }


    showStatus(message, type = 'info') {
        this.status.textContent = message;
        this.status.className = `status ${type}`;

        // Auto hide sau 5 giây cho message info
        if (type === 'info') {
            setTimeout(() => {
                if (this.status.textContent === message) {
                    this.status.textContent = '';
                    this.status.className = 'status';
                }
            }, 5000);
        }
    }

    // Cleanup khi trang được đóng
    cleanup() {
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
        }
    }
}

// Khởi tạo app khi trang load
document.addEventListener('DOMContentLoaded', () => {
    const app = new FaceDetectionApp();

    // Cleanup khi trang đóng
    window.addEventListener('beforeunload', () => {
        app.cleanup();
    });
});

// Xử lý lỗi CORS (nếu cần)
window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
    if (event.reason.message && event.reason.message.includes('CORS')) {
        document.getElementById('status').textContent = 'Lỗi CORS! Vui lòng kiểm tra cấu hình server.';
        document.getElementById('status').className = 'status error';
    }
});
