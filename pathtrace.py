# import core pox components
from pox.core import core
import pox.openflow.libopenflow_01 as of

# logger for printing output in terminal
log = core.getLogger()

# mac learning table
mac_to_port = {}

# path tracking
paths = {}

# this func runs everytime packet reaches controller
def _handle_PacketIn(event):
    # extract packet and switch details
    packet = event.parsed

    # switch id
    dpid = event.connection.dpid

    # initialise mac table if not there
    if dpid not in mac_to_port:
        mac_to_port[dpid] = {}

    in_port = event.port
    src = str(packet.src)  # src mac
    dst = str(packet.dst)  # dst mac

    # learn which port src mac connected to
    mac_to_port[dpid][src] = in_port

    # track switches for each src,dst pair
    key = (src, dst)

    if key not in paths:
        paths[key] = []

    if dpid not in paths[key]:
        paths[key].append(dpid)

    # if dst mac is known install flow route
    if dst in mac_to_port[dpid]:
        out_port = mac_to_port[dpid][dst]

        # create flow rule
        msg = of.ofp_flow_mod()

        # match fields
        msg.match.dl_src = packet.src
        msg.match.dl_dst = packet.dst

        # action: forward to correct port
        msg.actions.append(of.ofp_action_output(port=out_port))

        # send rule to switch
        event.connection.send(msg)

        # print path
        log.info("Flow installed : %s -> %s via %s",
                 src, dst,
                 "->".join("s" + str(x) for x in paths[key]))

        # send current packet also (important)
        msg2 = of.ofp_packet_out()
        msg2.data = event.ofp
        msg2.actions.append(of.ofp_action_output(port=out_port))
        event.connection.send(msg2)

    else:
        # flooding (unknown dest)
        msg = of.ofp_packet_out()
        msg.data = event.ofp

        # send packet to all ports
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        event.connection.send(msg)

        log.info("Flooding : %s -> %s at s%s", src, dst, dpid)


# launch function (entry point of pox)
def launch():
    # register packetin event handler
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)

    log.info("Path tracing tool started")
