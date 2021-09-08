
# def slice_name(name):
#     if '/' in name:
#         ind=name.index('/')
#         a=name[:ind]
#         if 'x'in a:
#             ind_x=a.index('x')
#             b=a[:ind_x]
#             h=''
#             for i in reversed(b[:-1]):
#                 h+=i
#             ind=h.index(' ')
#             a=h[ind:]
#             d=''
#             for i in reversed(a[:]):
#                 d+=i
#             return d.replace('"','').replace("''",'')
#         else:
#             return a.replace('"','').replace("''",'')  
#     else:
#         return name.replace('"','').replace("''",'')
# def full_name(names):
#     if 'Gb'in names:
#         gb_ind=names.index('Gb')
#         h=''
#         for i in reversed(names[:gb_ind]):
#             h+=i
#         pro_ind=h.index(' ')
#         a=''
#         c=h[pro_ind:]
#         for i in reversed(c):
#             a+=i
#         return(a)
#         # print(d)
#     elif "GB" in names:
#         gb_ind=names.index('GB')
#         h=''
#         for i in reversed(names[:gb_ind]):
#             h+=i
#         pro_ind=h.index(' ')
#         a=''
#         c=h[pro_ind:]
#         for i in reversed(c):
#             a+=i
#         return(a)
#     elif "Tb" in names:
#         gb_ind=names.index('Tb')
#         h=''
#         for i in reversed(names[:gb_ind]):
#             h+=i
#         pro_ind=h.index(' ')
#         a=''
#         c=h[pro_ind:]
#         for i in reversed(c):
#             a+=i
#         return(a)
#     elif "TB" in names:
#         gb_ind=names.index('TB')
#         h=''
#         for i in reversed(names[:gb_ind]):
#             h+=i
#         pro_ind=h.index(' ')
#         a=''
#         c=h[pro_ind:]
#         for i in reversed(c):
#             a+=i
#         return(a)
#     else:
#         return(names)
print('salom')