"""
Music Merger - 동영상 처리 엔진 (MoviePy 기반)
오디오 파일과 이미지를 결합하여 유튜브 업로드용 동영상 생성
"""

import os
import tempfile
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from moviepy import AudioFileClip, ImageClip

class VideoProcessor:
    """MoviePy 기반 동영상 파일 처리 클래스"""
    
    def __init__(self, console_log=None):
        self.console_log = console_log or print
        
    def log(self, message):
        """로그 메시지 출력"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.console_log(f"[{timestamp}] [VideoProcessor] {message}")
        
    def create_video_from_audio_image(self, audio_path, image_path, output_path, 
                                    video_size=(1920, 1080), fps=30, 
                                    progress_callback=None, add_brand_watermark=True,
                                    watermark_title=None):
        """
        오디오 파일과 이미지를 결합하여 동영상 생성
        
        Args:
            audio_path: 오디오 파일 경로 (.mp3, .wav 등)
            image_path: 이미지 파일 경로 (.jpg, .png 등)
            output_path: 출력 동영상 파일 경로 (.mp4)
            video_size: 동영상 해상도 (width, height)
            fps: 프레임 레이트
            progress_callback: 진행률 콜백 함수
            add_brand_watermark: 최종 영상에 OFF 워터마크 합성 여부
            watermark_title: 로고 아래에 표시할 트랙명 (생략 시 음원 파일명)
            
        Returns:
            dict: 생성 결과 정보
        """
        self.log(f"동영상 생성 시작: {os.path.basename(audio_path)} + {os.path.basename(image_path)}")
        
        # 파일 존재 여부 확인
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"오디오 파일을 찾을 수 없습니다: {audio_path}")
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"이미지 파일을 찾을 수 없습니다: {image_path}")
            
        try:
            if progress_callback:
                progress_callback(10, "오디오 파일 로딩 중...")
                
            # 오디오 클립 로드
            audio_clip = AudioFileClip(audio_path)
            audio_duration = audio_clip.duration
            self.log(f"오디오 길이: {audio_duration:.2f}초")
            
            if progress_callback:
                progress_callback(30, "이미지 처리 중...")
                
            # 이미지 전처리 (크기 조정)
            processed_image_path = self._resize_image(
                image_path,
                video_size,
                add_brand_watermark=add_brand_watermark,
                watermark_title=watermark_title or os.path.splitext(os.path.basename(audio_path))[0],
            )
            
            if progress_callback:
                progress_callback(50, "이미지 클립 생성 중...")
                
            # 이미지 클립 생성 (오디오 길이만큼)
            image_clip = ImageClip(processed_image_path, duration=audio_duration)
            image_clip = image_clip.with_fps(fps)
            
            if progress_callback:
                progress_callback(70, "오디오-비디오 결합 중...")
                
            # 오디오와 이미지 결합
            final_clip = image_clip.with_audio(audio_clip)
            
            if progress_callback:
                progress_callback(70, "동영상 파일 생성 중...")
            
            # MoviePy 진행률을 추정하는 간단한 방법
            import threading
            import time
            
            stop_monitoring = threading.Event()
            
            def monitor_file_progress():
                """출력 파일 크기를 모니터링하여 진행률 추정"""
                expected_size = None
                last_size = 0
                progress = 70
                
                while not stop_monitoring.is_set() and progress < 95:
                    try:
                        if os.path.exists(output_path):
                            current_size = os.path.getsize(output_path)
                            
                            # 파일 크기가 증가하고 있으면 진행 중
                            if current_size > last_size:
                                progress = min(progress + 2, 95)
                                if progress_callback:
                                    progress_callback(progress, f"동영상 생성 중... ({current_size // 1024}KB)")
                                last_size = current_size
                        
                        time.sleep(1)  # 1초마다 확인
                    except:
                        break
            
            # 파일 크기 모니터링 시작
            monitor_thread = threading.Thread(target=monitor_file_progress)
            monitor_thread.daemon = True
            monitor_thread.start()
            
            try:
                # 동영상 파일로 출력 (간단한 설정)
                final_clip.write_videofile(
                    output_path,
                    fps=fps,
                    codec='libx264',
                    audio_codec='aac',
                    temp_audiofile='temp-audio.m4a',
                    remove_temp=True,
                    preset='medium',
                    ffmpeg_params=[
                        '-crf', '23',
                        '-movflags', '+faststart'
                    ]
                )
            finally:
                # 모니터링 중지
                stop_monitoring.set()
                
            if progress_callback:
                progress_callback(95, "동영상 생성 완료 중...")
            
            # 메모리 정리
            audio_clip.close()
            image_clip.close()
            final_clip.close()
            
            # 임시 이미지 파일 정리 (약간의 지연 후)
            if processed_image_path != image_path:
                try:
                    import time
                    time.sleep(0.5)  # 파일 핸들이 완전히 해제될 때까지 대기
                    os.unlink(processed_image_path)
                except Exception as e:
                    self.log(f"임시 파일 삭제 실패 (무시됨): {str(e)}")
            
            if progress_callback:
                progress_callback(100, "완료!")
                
            # 결과 정보
            output_size = os.path.getsize(output_path)
            self.log(f"동영상 생성 완료: {output_path} ({output_size / (1024*1024):.1f}MB)")
            
            return {
                'success': True,
                'filename': os.path.basename(output_path),
                'duration': audio_duration,
                'size': output_size,
                'resolution': f"{video_size[0]}x{video_size[1]}",
                'fps': fps
            }
            
        except Exception as e:
            self.log(f"동영상 생성 실패: {str(e)}")
            raise
            
    def _resize_image(self, image_path, target_size, add_brand_watermark=True, watermark_title=None):
        """이미지 크기 조정 및 최적화"""
        self.log(f"이미지 크기 조정: {target_size}")
        
        try:
            with Image.open(image_path) as img:
                # RGBA를 RGB로 변환 (필요시)
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (0, 0, 0))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # 비율 유지하면서 크기 조정
                img_ratio = img.width / img.height
                target_ratio = target_size[0] / target_size[1]
                
                if img_ratio > target_ratio:
                    # 이미지가 더 넓음 - 높이 맞춤
                    new_height = target_size[1]
                    new_width = int(new_height * img_ratio)
                else:
                    # 이미지가 더 높음 - 너비 맞춤  
                    new_width = target_size[0]
                    new_height = int(new_width / img_ratio)
                
                # 리사이즈
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # 중앙 크롭
                left = (new_width - target_size[0]) // 2
                top = (new_height - target_size[1]) // 2
                right = left + target_size[0]
                bottom = top + target_size[1]
                
                img = img.crop((left, top, right, bottom))
                if add_brand_watermark:
                    self._add_brand_watermark(img, title=watermark_title)
                
                # 임시 파일로 저장
                temp_dir = os.path.dirname(image_path)
                temp_filename = f"temp_resized_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                temp_path = os.path.join(temp_dir, temp_filename)
                
                img.save(temp_path, 'JPEG', quality=95, optimize=True)
                
                self.log(f"이미지 처리 완료: {temp_path}")
                return temp_path
                
        except Exception as e:
            self.log(f"이미지 처리 실패: {str(e)}")
            # 원본 이미지 반환
            return image_path
            
    def get_video_presets(self):
        """유튜브 업로드용 동영상 프리셋"""
        return {
            'youtube_hd': {
                'size': (1920, 1080),
                'fps': 30,
                'description': '유튜브 HD (1080p)'
            },
            'youtube_hd_60': {
                'size': (1920, 1080), 
                'fps': 60,
                'description': '유튜브 HD 60fps (1080p)'
            },
            'youtube_standard': {
                'size': (1280, 720),
                'fps': 30,
                'description': '유튜브 표준 (720p)'
            },
            'youtube_mobile': {
                'size': (1280, 720),
                'fps': 30,
                'description': '모바일 최적화 (720p)'
            }
        }

    def create_default_cover(self, title, output_path, video_size=(1920, 1080), logo_path=None):
        """Create a clean branded 16:9 title card when audio has no artwork."""
        width, height = video_size
        title = (title or "Untitled track").strip()[:100]
        image = Image.new('RGB', (width, height), '#10131b')
        draw = ImageDraw.Draw(image)

        # A small deterministic-looking gradient makes the generated video usable
        # without requiring an image-generation API or an extra upload.
        for y in range(height):
            ratio = y / max(height - 1, 1)
            red = int(16 + 20 * ratio)
            green = int(19 + 14 * ratio)
            blue = int(27 + 44 * ratio)
            draw.line((0, y, width, y), fill=(red, green, blue))

        accent = '#ff5c7a'
        draw.ellipse((width * .58, height * .12, width * 1.05, height * .95), fill='#252d52')
        draw.ellipse((width * .68, height * .20, width * .98, height * .78), outline=accent, width=8)
        draw.rectangle((120, 160, 136, 720), fill=accent)
        draw.text((175, 166), 'OFF THE COMMUNITY', fill='#c9d1e6', font=self._font(28))
        draw.text((175, 245), 'NEW RELEASE', fill=accent, font=self._font(34))

        draw.text((175, height - 180), 'Official audio', fill='#c9d1e6', font=self._font(32))
        image.save(output_path, 'JPEG', quality=95, optimize=True)
        self.log(f"Default music-video cover created: {output_path}")
        return output_path

    @staticmethod
    def _add_brand_watermark(canvas, title=None, logo_path=None):
        """Composite the centered OFF logo plus restrained track title into each video frame."""
        if logo_path is None:
            logo_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'app', 'Frame 1.png'
            )
        if not os.path.isfile(logo_path):
            return

        try:
            with Image.open(logo_path) as source:
                watermark = source.convert('RGBA')
                target_width = max(190, min(330, canvas.width // 5))
                target_height = round(watermark.height * target_width / watermark.width)
                watermark = watermark.resize((target_width, target_height), Image.Resampling.LANCZOS)

                # The source asset has a transparent background. Preserve it,
                # while keeping the mark present but secondary to the track title.
                alpha = watermark.getchannel('A').point(lambda value: int(value * 0.78))
                watermark.putalpha(alpha)
                position = (
                    (canvas.width - target_width) // 2,
                    # Keep the logo itself on the visual centreline, matching
                    # the existing OFF official-audio artwork. The title then
                    # sits naturally below without making the mark look high.
                    max(80, int(canvas.height * .35)),
                )
                canvas.paste(watermark, position, watermark)

                clean_title = (title or '').strip()[:100]
                if not clean_title:
                    return
                title_font = VideoProcessor._brand_font(max(44, canvas.width // 46 + 10))
                title_layer = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
                title_draw = ImageDraw.Draw(title_layer)
                lines = VideoProcessor._wrap_title(
                    title_draw, clean_title, title_font, max_width=int(canvas.width * .48)
                )[:2]
                y = position[1] + target_height + max(22, canvas.height // 48)
                for line in lines:
                    bbox = title_draw.textbbox((0, 0), line, font=title_font)
                    x = (canvas.width - (bbox[2] - bbox[0])) // 2
                    # A quiet shadow keeps the title readable on light artwork.
                    title_draw.text((x + 2, y + 3), line, fill=(0, 0, 0, 105), font=title_font)
                    title_draw.text((x, y), line, fill=(245, 242, 232, 225), font=title_font)
                    y += (bbox[3] - bbox[1]) + max(10, canvas.height // 90)
                canvas.paste(title_layer, (0, 0), title_layer)
        except Exception as error:
            # Branding should never prevent a creator's video from rendering.
            self.log(f"Brand watermark skipped: {error}")

    @staticmethod
    def _font(size):
        """Use a common bold system font, with Pillow's default as a safe fallback."""
        for path in (
            '/System/Library/Fonts/Supplemental/Arial Bold.ttf',
            '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
            'C:/Windows/Fonts/arialbd.ttf',
        ):
            if os.path.exists(path):
                return ImageFont.truetype(path, size)
        return ImageFont.load_default()

    @staticmethod
    def _brand_font(size):
        """Use Apple SD Gothic Neo Medium for the clean Korean/English wordmark style."""
        try:
            return ImageFont.truetype('/System/Library/Fonts/AppleSDGothicNeo.ttc', size, index=2)
        except OSError:
            return VideoProcessor._font(size)

    @staticmethod
    def _wrap_title(draw, title, font, max_width):
        words = title.split() or [title]
        lines, current = [], ''
        for word in words:
            candidate = f"{current} {word}".strip()
            if current and draw.textbbox((0, 0), candidate, font=font)[2] > max_width:
                lines.append(current)
                current = word
            else:
                current = candidate
        if current:
            lines.append(current)
        return lines[:3]
        
    def estimate_processing_time(self, audio_duration):
        """
        예상 처리 시간 계산
        
        Args:
            audio_duration: 오디오 길이 (초)
            
        Returns:
            예상 처리 시간 (초)
        """
        # MoviePy는 실시간의 1.5-2배 정도 소요
        return max(audio_duration * 1.8, 30)  # 최소 30초
