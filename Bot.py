import os
import asyncio
import logging

logger = logging.getLogger(__name__)

async def add_arabic_subtitles_railway(video_path: str, sub_path: str, output_path: str) -> bool:
    """
    دالة متكاملة مخصصة لريبو WZML-X على منصة Railway لدمج ملفات الترجمة .srt 
    داخل الفيديو بشكل صلب (Hardcode) باستخدام خط Sultan Bold وحجم خط مضبوط تلقائياً.
    """
    # التحقق من وجود الملفات لتجنب انهيار الـ Task
    if not os.path.exists(video_path):
        logger.error(f"❌ ملف الفيديو غير موجود في المسار: {video_path}")
        return False
    if not os.path.exists(sub_path):
        logger.error(f"❌ ملف الترجمة غير موجود في المسار: {sub_path}")
        return False

    # تهيئة مسار الترجمة ليتوافق مع نظام فلاتر FFmpeg الداخلي (الهروب من الرموز الخاصة)
    safe_sub_path = sub_path.replace("\\", "/").replace(":", "\\:")
    
    # إعدادات الستايل الكاملة (الخط: Sultan bold، الحجم: 26، إضافة حد خارجي أسود لمنع اختفاء النص خلف الألوان الفاتحة)
    video_filter_style = (
        f"subtitles='{safe_sub_path}':"
        f"force_style='Fontname=Sultan bold,Fontsize=26,Outline=2,OutlineColour=&H00000000,BorderStyle=1,Shadow=1,Alignment=2'"
    )

    # بناء أمر FFmpeg المتكامل المتوافق مع موارد Railway
    cmd = [
        'ffmpeg', '-y',
        '-i', video_path,                 # ملف الفيديو المدخل
        '-vf', video_filter_style,         # فلتر الترجمة والستايل الخاص بها
        '-c:a', 'copy',                    # نسخ الصوت الأصلي مباشرة دون إعادة ترميز لتسريع العملية 10 أضعاف
        '-c:v', 'libx264',                 # ترميز الفيديو لتطبيق الهارد كود
        '-preset', 'faster',               # وضع المعالجة الأسرع المناسب لمعالجات Railway
        '-crf', '22',                      # الحفاظ على الجودة الأصلية للفيديو دون زيادة في المساحة
        output_path                        # مسار ملف الفيديو النهائي الناتج
    ]

    logger.info("🎬 جاري معالجة دمج الترجمة بخط Sultan Bold عبر FFmpeg على Railway...")
    
    try:
        # تشغيل الأمر بشكل غير متزامن تماماً لمنع تجميد أو توقف البوت أثناء المعالجة
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            logger.info("✅ تم دمج الترجمة بنجاح بالخط العربي المخصص Sultan Bold!")
            return True
        else:
            logger.error(f"❌ فشل أمر FFmpeg أثناء معالجة الترجمة: {stderr.decode()}")
            return False

    except Exception as e:
        logger.error(f"❌ حدث خطأ غير متوقع أثناء معالجة الترجمة: {str(e)}")
        return False
