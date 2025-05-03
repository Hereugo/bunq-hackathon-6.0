import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3';
import { NextResponse } from 'next/server';
import { z } from 'zod';

import { auth } from '@/app/(auth)/auth';

// Use Blob instead of File since File is not available in Node.js environment
const FileSchema = z.object({
  file: z
    .instanceof(Blob)
    .refine((file) => file.size <= 5 * 1024 * 1024, {
      message: 'File size should be less than 5MB',
    })
    // Update the file type based on the kind of files you want to accept
    .refine((file) => ['image/jpeg', 'image/png'].includes(file.type), {
      message: 'File type should be JPEG or PNG',
    }),
});

// Initialize MinIO S3 client
const s3Client = new S3Client({
  region: 'us-east-1', // MinIO doesn't require a specific region, but S3 client needs one
  endpoint: process.env.BLOB_STORAGE_ENDPOINT || 'http://minio:9000',
  credentials: {
    accessKeyId: process.env.BLOB_STORAGE_ACCESS_KEY || 'minioadmin',
    secretAccessKey: process.env.BLOB_STORAGE_SECRET_KEY || 'minioadmin',
  },
  forcePathStyle: true, // Required for MinIO
});

export async function POST(request: Request) {
  const session = await auth();

  if (!session) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  if (request.body === null) {
    return new Response('Request body is empty', { status: 400 });
  }

  try {
    const formData = await request.formData();
    const file = formData.get('file') as Blob;

    if (!file) {
      return NextResponse.json({ error: 'No file uploaded' }, { status: 400 });
    }

    const validatedFile = FileSchema.safeParse({ file });

    if (!validatedFile.success) {
      const errorMessage = validatedFile.error.errors
        .map((error) => error.message)
        .join(', ');

      return NextResponse.json({ error: errorMessage }, { status: 400 });
    }

    // Get filename from formData since Blob doesn't have name property
    const filename = (formData.get('file') as File).name;
    const fileBuffer = await file.arrayBuffer();

    // Ensure unique filenames by adding a timestamp
    const uniqueFilename = `${Date.now()}-${filename}`;
    const bucketName = process.env.BLOB_STORAGE_BUCKET || 'app-bucket';

    try {
      // Upload file to MinIO
      const uploadParams = {
        Bucket: bucketName,
        Key: uniqueFilename,
        Body: Buffer.from(fileBuffer),
        ContentType: file.type,
      };

      const uploadCommand = new PutObjectCommand(uploadParams);
      await s3Client.send(uploadCommand);

      // Generate the file URL
      // Replace internal Docker hostname with publicly accessible URL
      // This uses the current request host or falls back to localhost
      const publicEndpoint =
        process.env.NEXT_PUBLIC_BLOB_STORAGE_ENDPOINT ||
        (request.headers.get('host')
          ? `http://${request.headers.get('host')?.split(':')[0]}:9000`
          : 'http://localhost:9000');

      const fileUrl = `${publicEndpoint}/${bucketName}/${uniqueFilename}`;

      return NextResponse.json({
        url: fileUrl,
        pathname: `/${bucketName}/${uniqueFilename}`,
        contentType: file.type,
        size: file.size,
      });
    } catch (error) {
      console.error('Upload error:', error);
      return NextResponse.json({ error: 'Upload failed' }, { status: 500 });
    }
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to process request' },
      { status: 500 },
    );
  }
}
