from django.http import HttpResponseForbidden

class AuthorizationMiddleware:
    def _init_(self, get_response):
        self.get_response = get_response

    def _call_(self, request):
        # Membaca data pengguna
        user = request.user

        # Lakukan pengecekan autorisasi berdasarkan data pengguna di sini
        if not user.is_authenticated:
            return HttpResponseForbidden("Anda tidak diizinkan mengakses halaman ini.")
        
        # Mengakses atribut data pengguna
        username = user.username
        email = user.email

        return self.get_response(request)