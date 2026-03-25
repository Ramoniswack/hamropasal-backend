from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import Order, OrderStatusHistory


@receiver(post_save, sender=Order)
def send_order_confirmation_email(sender, instance, created, **kwargs):
    """
    Send order confirmation email to customer when order is created
    Also notify admin about new order
    """
    if created:
        # Send email to customer
        subject = f'Order Confirmation - {instance.order_number}'
        
        # HTML email content
        html_message = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
                <h2 style="color: #4CAF50; text-align: center;">Order Confirmed! 🎉</h2>
                
                <p>Dear {instance.customer_name},</p>
                
                <p>Thank you for your order! We've received your order and it's being processed.</p>
                
                <div style="background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h3 style="margin-top: 0;">Order Details:</h3>
                    <p><strong>Order Number:</strong> {instance.order_number}</p>
                    <p><strong>Order Date:</strong> {instance.created_at.strftime('%B %d, %Y at %I:%M %p')}</p>
                    <p><strong>Total Amount:</strong> Rs. {instance.total}</p>
                    <p><strong>Status:</strong> <span style="color: #FF9800; font-weight: bold;">{instance.get_status_display()}</span></p>
                </div>
                
                <div style="background: #e3f2fd; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h3 style="margin-top: 0;">Shipping Address:</h3>
                    <p>
                        {instance.customer_name}<br>
                        {instance.shipping_address}<br>
                        {instance.shipping_city}, {instance.shipping_state} {instance.shipping_zip_code}<br>
                        {instance.shipping_country}<br>
                        Phone: {instance.customer_phone}
                    </p>
                </div>
                
                <div style="background: #fff3cd; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h3 style="margin-top: 0;">Order Items:</h3>
                    <table style="width: 100%; border-collapse: collapse;">
                        <thead>
                            <tr style="background: #f5f5f5;">
                                <th style="padding: 8px; text-align: left; border-bottom: 2px solid #ddd;">Product</th>
                                <th style="padding: 8px; text-align: center; border-bottom: 2px solid #ddd;">Qty</th>
                                <th style="padding: 8px; text-align: right; border-bottom: 2px solid #ddd;">Price</th>
                            </tr>
                        </thead>
                        <tbody>
                            {''.join([f'''
                            <tr>
                                <td style="padding: 8px; border-bottom: 1px solid #eee;">{item.product_name}</td>
                                <td style="padding: 8px; text-align: center; border-bottom: 1px solid #eee;">{item.quantity}</td>
                                <td style="padding: 8px; text-align: right; border-bottom: 1px solid #eee;">Rs. {item.subtotal}</td>
                            </tr>
                            ''' for item in instance.items.all()])}
                        </tbody>
                        <tfoot>
                            <tr>
                                <td colspan="2" style="padding: 8px; text-align: right; font-weight: bold;">Subtotal:</td>
                                <td style="padding: 8px; text-align: right; font-weight: bold;">Rs. {instance.subtotal}</td>
                            </tr>
                            <tr>
                                <td colspan="2" style="padding: 8px; text-align: right;">Shipping:</td>
                                <td style="padding: 8px; text-align: right;">Rs. {instance.shipping_cost}</td>
                            </tr>
                            <tr style="background: #f5f5f5;">
                                <td colspan="2" style="padding: 8px; text-align: right; font-weight: bold; font-size: 18px;">Total:</td>
                                <td style="padding: 8px; text-align: right; font-weight: bold; font-size: 18px; color: #4CAF50;">Rs. {instance.total}</td>
                            </tr>
                        </tfoot>
                    </table>
                </div>
                
                <p style="margin-top: 30px;">We'll send you another email when your order ships.</p>
                
                <p>If you have any questions, please don't hesitate to contact us.</p>
                
                <p style="margin-top: 30px;">
                    Best regards,<br>
                    <strong>Hamro Pasal Team</strong>
                </p>
                
                <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
                
                <p style="font-size: 12px; color: #999; text-align: center;">
                    This is an automated email. Please do not reply to this email.
                </p>
            </div>
        </body>
        </html>
        """
        
        plain_message = strip_tags(html_message)
        
        try:
            # Send to customer
            email = EmailMultiAlternatives(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [instance.customer_email]
            )
            email.attach_alternative(html_message, "text/html")
            email.send(fail_silently=False)
            
            # Notify admin about new order
            admin_subject = f'New Order Received - {instance.order_number}'
            admin_message = f"""
            New order received!
            
            Order Number: {instance.order_number}
            Customer: {instance.customer_name}
            Email: {instance.customer_email}
            Phone: {instance.customer_phone}
            Total Amount: Rs. {instance.total}
            
            Please log in to the admin panel to process this order.
            """
            
            send_mail(
                admin_subject,
                admin_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],
                fail_silently=True
            )
            
        except Exception as e:
            # Log error but don't fail the order creation
            print(f"Error sending order confirmation email: {e}")


@receiver(post_save, sender=OrderStatusHistory)
def send_order_status_update_email(sender, instance, created, **kwargs):
    """
    Send email to customer when order status changes
    """
    if created and instance.order.customer_email:
        order = instance.order
        status = instance.status
        
        # Define status-specific messages
        status_messages = {
            'confirmed': {
                'title': 'Order Confirmed',
                'emoji': '✅',
                'message': 'Your order has been confirmed and is being prepared for shipment.',
                'color': '#4CAF50'
            },
            'processing': {
                'title': 'Order Processing',
                'emoji': '⚙️',
                'message': 'Your order is currently being processed.',
                'color': '#2196F3'
            },
            'shipped': {
                'title': 'Order Shipped',
                'emoji': '🚚',
                'message': 'Great news! Your order has been shipped and is on its way to you.',
                'color': '#FF9800'
            },
            'delivered': {
                'title': 'Order Delivered',
                'emoji': '📦',
                'message': 'Your order has been successfully delivered. We hope you enjoy your purchase!',
                'color': '#4CAF50'
            },
            'cancelled': {
                'title': 'Order Cancelled',
                'emoji': '❌',
                'message': 'Your order has been cancelled. If you have any questions, please contact us.',
                'color': '#f44336'
            },
        }
        
        status_info = status_messages.get(status, {
            'title': 'Order Status Update',
            'emoji': '📋',
            'message': f'Your order status has been updated to: {order.get_status_display()}',
            'color': '#9E9E9E'
        })
        
        subject = f"{status_info['emoji']} {status_info['title']} - {order.order_number}"
        
        html_message = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
                <h2 style="color: {status_info['color']}; text-align: center;">{status_info['emoji']} {status_info['title']}</h2>
                
                <p>Dear {order.customer_name},</p>
                
                <p>{status_info['message']}</p>
                
                <div style="background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h3 style="margin-top: 0;">Order Details:</h3>
                    <p><strong>Order Number:</strong> {order.order_number}</p>
                    <p><strong>Order Date:</strong> {order.created_at.strftime('%B %d, %Y')}</p>
                    <p><strong>Total Amount:</strong> Rs. {order.total}</p>
                    <p><strong>Current Status:</strong> <span style="color: {status_info['color']}; font-weight: bold;">{order.get_status_display()}</span></p>
                </div>
                
                {f'''
                <div style="background: #e8f5e9; padding: 15px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #4CAF50;">
                    <p style="margin: 0;"><strong>📝 Note from Admin:</strong></p>
                    <p style="margin: 10px 0 0 0;">{instance.notes}</p>
                </div>
                ''' if instance.notes else ''}
                
                <p style="margin-top: 30px;">You can track your order status anytime by logging into your account.</p>
                
                <p>If you have any questions, please don't hesitate to contact us.</p>
                
                <p style="margin-top: 30px;">
                    Best regards,<br>
                    <strong>Hamro Pasal Team</strong>
                </p>
                
                <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
                
                <p style="font-size: 12px; color: #999; text-align: center;">
                    This is an automated email. Please do not reply to this email.
                </p>
            </div>
        </body>
        </html>
        """
        
        plain_message = strip_tags(html_message)
        
        try:
            email = EmailMultiAlternatives(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [order.customer_email]
            )
            email.attach_alternative(html_message, "text/html")
            email.send(fail_silently=False)
            
        except Exception as e:
            # Log error but don't fail the status update
            print(f"Error sending order status update email: {e}")
