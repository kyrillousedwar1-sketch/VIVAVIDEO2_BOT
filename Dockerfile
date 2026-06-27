FROM anonym7/wzml-x:master

# تثبيت الحزم اللازمة لإدارة الخطوط داخل السيرفر
RUN apt-get update && apt-get install -y fontconfig font-manager

# إنشاء مجلد الخطوط المخصصة ونقل خط Sultan Bold إليه
RUN mkdir -p /usr/share/fonts/truetype/sultan
COPY Sultan-bold.ttf /usr/share/fonts/truetype/sultan/

# تحديث كاش خطوط النظام ليتعرف FFmpeg على اسم الخط "Sultan bold"
RUN fc-cache -fv

# استكمال تشغيل الريبو الأصلي
CMD ["python3", "-m", "bot"]
