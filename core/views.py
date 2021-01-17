from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def test(request):
    import matplotlib.pyplot as plt
    import cv2
    part = int(request.query_params.get('part'))
    im = cv2.imread(request.query_params.get('name'))
    M = im.shape[0]
    N = im.shape[1] // part
    tiles = [im[x:x + M, y:y + N] for x in range(0, im.shape[0], M) for y in range(0, im.shape[1], N)]
    bs = []
    for i in range(part):
        f = plt.figure()
        vals = tiles[i].mean(axis=2).flatten()
        b, bins, patches = plt.hist(vals, 255)
        bs.append(b)
        ## SAVE IMAGE PART
        from PIL import Image
        im = Image.fromarray(tiles[i])
        im.save("your_file{}.jpeg".format(str(i)))

        ## SAVE PLT
        # plt.xlim([0, 255])
        # plt.show()
        # f.savefig("/home/oleg/Рабочий стол/{}.pdf".format(str(i)), bbox_inches='tight')

    for j in range(1, len(bs)):
        s = 0
        for i in range(len(bs[j])):
            # if bs[0][i] >= 0.1 and bs[j][i] >= 0.1:
            #     if abs(bs[0][i] - bs[j][i]) > 10.0:
            #         # 5%
            #         if abs(bs[0][i] - bs[j][i]) > (bs[0][i] + bs[j][i]) / 40:
            if not check(bs[0][i], bs[j][i]):
                pre = True
                pos = True
                if i > 0:
                    pre = check(bs[0][i - 1], bs[j][i - 1])
                if i < len(bs[0]) - 1:
                    pos = check(bs[0][i + 1], bs[j][i + 1])
                if not pre and not pos:
                    s += 1
                    if s * 10 > len(bs[j]):
                        print("BAD" + str(abs(bs[0][i] - bs[j][i])))
                        print("j " + str(i))
                        print("bs[0][i] " + str(bs[0][i]))
                        print("bs[j][i] " + str(bs[j][i]))
                        return Response({'Gamogen': "NOT"}, status=status.HTTP_200_OK)

    return Response({'Gamogen': "YES"}, status=status.HTTP_200_OK)


def check(a1, a2):
    if a1 >= 0.1 and a2 >= 0.1:
        if abs(a1 - a2) > 5.0:
            # 10%
            if abs(a1 - a2) > (a1 + a2) / 20:
                return False
    return True