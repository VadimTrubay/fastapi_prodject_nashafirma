# import hashlib
# from uuid import uuid4
#
# import cloudinary
# import cloudinary.uploader
# from nashafirma_fastapi.conf.config import settings
#
#
# class CloudImage:
#     cloudinary.config(
#         cloud_name=settings.cloudinary_name,
#         api_key=settings.cloudinary_api_key,
#         api_secret=settings.cloudinary_api_secret,
#         secure=True
#     )
#
#     @staticmethod
#     def generate_name_avatar(email: str):
#         name = hashlib.sha256(email.encode('utf-8')).hexdigest()[:12]
#         return f"user{name}"
#
#     @staticmethod
#     def upload(file, public_id: str, overwrite=True):
#         r = cloudinary.uploader.upload(file, public_id=public_id, overwrite=overwrite)
#         return r
#
#     @staticmethod
#     def get_url_for_avatar(public_id, r):
#         src_url = cloudinary.CloudinaryImage(public_id) \
#             .build_url(width=250, height=250, crop='fill', version=r.get('version'))
#         return src_url
#
#     @staticmethod
#     def get_url_for_image(file_name):
#         src_url = cloudinary.utils.cloudinary_url(file_name)
#         return src_url[0]
