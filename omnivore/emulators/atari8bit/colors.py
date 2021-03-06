import numpy as np

NTSC = np.array([
(15, 15, 15, 255), (31, 31, 31, 255), (47, 47, 47, 255), (63, 63, 63, 255), (79, 79, 79, 255), (95, 95, 95, 255), (111, 111, 111, 255), (127, 127, 127, 255), (143, 143, 143, 255), (159, 159, 159, 255), (175, 175, 175, 255), (191, 191, 191, 255), (207, 207, 207, 255), (223, 223, 223, 255), (239, 239, 239, 255), (255, 255, 255, 255), (20, 36, 0, 255), (36, 52, 0, 255), (52, 68, 0, 255), (68, 84, 0, 255), (84, 100, 0, 255), (100, 116, 0, 255), (116, 132, 0, 255), (132, 148, 4, 255), (148, 164, 20, 255), (164, 180, 36, 255), (180, 196, 52, 255), (196, 212, 68, 255), (212, 228, 84, 255), (228, 244, 100, 255), (244, 255, 116, 255), (255, 255, 132, 255), (58, 12, 0, 255), (74, 28, 0, 255), (90, 44, 0, 255), (106, 60, 0, 255), (122, 76, 0, 255), (138, 92, 0, 255), (154, 108, 10, 255), (170, 124, 26, 255), (186, 140, 42, 255), (202, 156, 58, 255), (218, 172, 74, 255), (234, 188, 90, 255), (250, 204, 106, 255), (255, 220, 122, 255), (255, 236, 138, 255), (255, 252, 154, 255), (79, 0, 0, 255), (95, 8, 0, 255), (111, 24, 0, 255), (127, 40, 8, 255), (143, 56, 24, 255), (159, 72, 40, 255), (175, 88, 56, 255), (191, 104, 72, 255), (207, 120, 88, 255), (223, 136, 104, 255), (239, 152, 120, 255), (255, 168, 136, 255), (255, 184, 152, 255), (255, 200, 168, 255), (255, 216, 184, 255), (255, 232, 200, 255), (87, 0, 6, 255), (103, 0, 22, 255), (119, 11, 38, 255), (135, 27, 54, 255), (151, 43, 70, 255), (167, 59, 86, 255), (183, 75, 102, 255), (199, 91, 118, 255), (215, 107, 134, 255), (231, 123, 150, 255), (247, 139, 166, 255), (255, 155, 182, 255), (255, 171, 198, 255), (255, 187, 214, 255), (255, 203, 230, 255), (255, 219, 246, 255), (77, 0, 75, 255), (93, 0, 91, 255), (109, 3, 107, 255), (125, 19, 123, 255), (141, 35, 139, 255), (157, 51, 155, 255), (173, 67, 171, 255), (189, 83, 187, 255), (205, 99, 203, 255), (221, 115, 219, 255), (237, 131, 235, 255), (253, 147, 251, 255), (255, 163, 255, 255), (255, 179, 255, 255), (255, 195, 255, 255), (255, 211, 255, 255), (57, 0, 110, 255), (73, 0, 126, 255), (89, 7, 142, 255), (105, 23, 158, 255), (121, 39, 174, 255), (137, 55, 190, 255), (153, 71, 206, 255), (169, 87, 222, 255), (185, 103, 238, 255), (201, 119, 254, 255), (217, 135, 255, 255), (233, 151, 255, 255), (249, 167, 255, 255), (255, 183, 255, 255), (255, 199, 255, 255), (255, 215, 255, 255), (29, 0, 118, 255), (45, 3, 134, 255), (61, 19, 150, 255), (77, 35, 166, 255), (93, 51, 182, 255), (109, 67, 198, 255), (125, 83, 214, 255), (141, 99, 230, 255), (157, 115, 246, 255), (173, 131, 255, 255), (189, 147, 255, 255), (205, 163, 255, 255), (221, 179, 255, 255), (237, 195, 255, 255), (253, 211, 255, 255), (255, 227, 255, 255), (2, 2, 112, 255), (18, 18, 128, 255), (34, 34, 144, 255), (50, 50, 160, 255), (66, 66, 176, 255), (82, 82, 192, 255), (98, 98, 208, 255), (114, 114, 224, 255), (130, 130, 240, 255), (146, 146, 255, 255), (162, 162, 255, 255), (178, 178, 255, 255), (194, 194, 255, 255), (210, 210, 255, 255), (226, 226, 255, 255), (242, 242, 255, 255), (0, 17, 93, 255), (0, 33, 109, 255), (12, 49, 125, 255), (28, 65, 141, 255), (44, 81, 157, 255), (60, 97, 173, 255), (76, 113, 189, 255), (92, 129, 205, 255), (108, 145, 221, 255), (124, 161, 237, 255), (140, 177, 253, 255), (156, 193, 255, 255), (172, 209, 255, 255), (188, 225, 255, 255), (204, 241, 255, 255), (220, 255, 255, 255), (0, 30, 54, 255), (0, 46, 70, 255), (0, 62, 86, 255), (16, 78, 102, 255), (32, 94, 118, 255), (48, 110, 134, 255), (64, 126, 150, 255), (80, 142, 166, 255), (96, 158, 182, 255), (112, 174, 198, 255), (128, 190, 214, 255), (144, 206, 230, 255), (160, 222, 246, 255), (176, 238, 255, 255), (192, 254, 
    255, 255), (208, 255, 255, 255), (0, 40, 9, 255), (0, 56, 25, 255), (0, 72, 41, 255), (14, 88, 57, 255), (30, 104, 73, 255), (46, 120, 89, 255), (62, 136, 105, 255), (78, 152, 121, 255), (94, 168, 137, 255), (110, 184, 153, 255), (126, 200, 169, 255), (142, 216, 185, 255), (158, 232, 201, 255), (174, 248, 217, 255), (190, 255, 233, 255), (206, 255, 249, 255), (0, 44, 0, 255), (0, 60, 0, 255), (6, 76, 1, 255), (22, 92, 17, 255), (38, 108, 33, 255), (54, 124, 49, 255), (70, 140, 65, 255), (86, 156, 81, 255), (102, 172, 97, 255), (118, 188, 113, 255), (134, 204, 129, 255), (150, 220, 145, 255), (166, 236, 161, 255), (182, 252, 177, 255), (198, 255, 193, 255), (214, 255, 209, 255), (0, 40, 0, 255), (7, 56, 0, 255), (23, 72, 0, 255), (39, 88, 0, 255), (55, 104, 8, 255), (71, 120, 24, 255), (87, 136, 40, 255), (103, 152, 56, 255), (119, 168, 72, 255), (135, 184, 88, 255), (151, 200, 104, 255), (167, 216, 120, 255), (183, 232, 136, 255), (199, 248, 152, 255), (215, 255, 168, 255), (231, 255, 184, 255), (12, 30, 0, 255), (28, 46, 0, 255), (44, 62, 0, 255), (60, 78, 0, 255), (76, 94, 4, 255), (92, 110, 20, 255), (108, 126, 36, 255), (124, 142, 52, 255), (140, 158, 68, 255), (156, 174, 84, 255), (172, 190, 100, 255), (188, 206, 116, 255), (204, 222, 132, 255), (220, 238, 148, 255), (236, 254, 164, 255), (252, 255, 180, 255), (31, 21, 0, 255), (47, 37, 0, 255), (63, 53, 0, 255), (79, 69, 0, 255), (95, 85, 5, 255), (111, 101, 21, 255), (127, 117, 37, 255), (143, 133, 53, 255), (159, 149, 69, 255), (175, 165, 85, 255), (191, 181, 101, 255), (207, 197, 117, 255), (223, 213, 133, 255), (239, 229, 149, 255), (255, 245, 165, 255), (255, 255, 181, 255), ], dtype=np.uint8)
