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
            const response = await fetch('http://localhost:5000/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    image: this.capturedImageData
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

        if (!data.faces || data.faces.length === 0) {
            this.showStatus('Không phát hiện khuôn mặt nào trong ảnh!', 'error');
            return;
        }

        // Hiển thị kết quả cho từng khuôn mặt
        data.faces.forEach((face, index) => {
            const faceDiv = document.createElement('div');
            faceDiv.className = `face-result ${face.is_real ? 'real' : 'spoof'}`;

            const isRealText = face.is_real ? '✅ THẬT' : '❌ GIẢ MẠO';
            const confidence = Math.round(face.det_conf * 100);
            const spoofScore = Math.round(face.spoof_score * 100);

            faceDiv.innerHTML = `
                <h4>Khuôn mặt ${index + 1}</h4>
                <div class="result-item">
                    <span class="result-label">Trạng thái:</span>
                    <span class="result-value" style="color: ${face.is_real ? '#4CAF50' : '#f44336'}; font-weight: bold;">
                        ${isRealText}
                    </span>
                </div>
                <div class="result-item">
                    <span class="result-label">Độ tin cậy phát hiện:</span>
                    <span class="result-value">${confidence}%</span>
                </div>
                <div class="result-item">
                    <span class="result-label">Điểm số chống giả mạo:</span>
                    <span class="result-value">${spoofScore}%</span>
                </div>
                <div class="result-item">
                    <span class="result-label">Vị trí:</span>
                    <span class="result-value">x:${face.box.x}, y:${face.box.y}, w:${face.box.w}, h:${face.box.h}</span>
                </div>
            `;

            this.faceResults.appendChild(faceDiv);
        });

        const realFaces = data.faces.filter(face => face.is_real).length;
        const totalFaces = data.faces.length;

        if (realFaces === totalFaces) {
            this.showStatus(`✅ Phân tích thành công! Tất cả ${totalFaces} khuôn mặt đều là thật.`, 'success');
        } else {
            this.showStatus(`⚠️ Phát hiện ${totalFaces - realFaces}/${totalFaces} khuôn mặt giả mạo!`, 'error');
        }
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
