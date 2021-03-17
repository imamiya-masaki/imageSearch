import cloudinary
import cloudinary.uploader
import cloudinary.api
import secrets
cloudinary.config(
  cloud_name = "dklrtv3fr",
  api_key = "155243477797553",
  api_secret = "FS2edonBgsL_D9HjHErVGgTS6-U"
)
def uploadImage(image):
    id = secrets.token_hex(10)
    res = cloudinary.uploader.upload(file=image, public_id=id)
    print("res", res)
    return id
