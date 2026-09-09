from pydantic import BaseModel, Field
from typing import Optional

class LoginRequest(BaseModel):
    username: str = Field(
        ..., 
        example="22101152630449",  # Tambahkan contoh
        description="NIM/NPM atau username"
    )
    password: str = Field(
        ..., 
        example="2213669NA",  # Tambahkan contoh
        description="Password SISFO"
    )

class JadwalRequest(BaseModel):
    semester: Optional[str] = Field(
        None, 
        example="20241",
        description="Semester (contoh: 20241 untuk semester ganjil 2024/2025)"
    )

class NilaiRequest(BaseModel):
    semester: Optional[str] = Field(
        None, 
        example="20241",
        description="Semester (contoh: 20241 untuk semester ganjil 2024/2025)"
    )

class AbsensiRequest(BaseModel):
    from_date: Optional[str] = Field(
        None, 
        example="2026-01-01",
        description="Tanggal mulai (YYYY-MM-DD)"
    )
    to_date: Optional[str] = Field(
        None, 
        example="2026-12-31",
        description="Tanggal akhir (YYYY-MM-DD)"
    )

class KRSRequest(BaseModel):
    semester: Optional[str] = Field(
        None, 
        example="20241",
        description="Semester (contoh: 20241 untuk semester ganjil 2024/2025)"
    )